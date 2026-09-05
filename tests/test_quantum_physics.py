"""Tests for reading Quantum-Physics's encrypted preference file and login."""

import base64
import json
import pathlib
import tempfile
import unittest

from unittest import mock

from physicslab import quantum_physics
from physicslab import web


# Source indexes of the forward ShiftRows transform in Rijndael's
# column-major state (row *r* is shifted left by *r* columns).
_SHIFT_ROWS = (0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11)


def _encrypt_mix_columns(state):
    for column in range(4):
        offset = 4 * column
        a0 = state[offset]
        a1 = state[offset + 1]
        a2 = state[offset + 2]
        a3 = state[offset + 3]
        x2 = quantum_physics._xtime
        state[offset] = x2(a0) ^ x2(a1) ^ a1 ^ a2 ^ a3
        state[offset + 1] = a0 ^ x2(a1) ^ x2(a2) ^ a2 ^ a3
        state[offset + 2] = a0 ^ a1 ^ x2(a2) ^ x2(a3) ^ a3
        state[offset + 3] = x2(a0) ^ a0 ^ a1 ^ a2 ^ x2(a3)


def _encrypt_block(block, expanded_key):
    state = list(block)
    quantum_physics._add_round_key(state, expanded_key, 0)
    for round_index in range(1, quantum_physics._RIJNDAEL_ROUNDS):
        state = [quantum_physics._SBOX[value] for value in state]
        state = [state[source] for source in _SHIFT_ROWS]
        _encrypt_mix_columns(state)
        quantum_physics._add_round_key(state, expanded_key, round_index)
    state = [quantum_physics._SBOX[value] for value in state]
    state = [state[source] for source in _SHIFT_ROWS]
    quantum_physics._add_round_key(
        state, expanded_key, quantum_physics._RIJNDAEL_ROUNDS
    )
    return bytes(state)


def _encrypt_preference(plaintext):
    """Encrypt *plaintext* with the game's scheme (test-only mirror)."""
    key = bytes.fromhex(quantum_physics._CACHE_PASSWORD_HEX)
    iv = key + key
    expanded_key = quantum_physics._expand_game_key(key)
    block_size = quantum_physics._BLOCK_SIZE
    pad_length = block_size - len(plaintext) % block_size
    plaintext += bytes([pad_length]) * pad_length

    ciphertext = bytearray()
    previous = iv
    for offset in range(0, len(plaintext), block_size):
        block = plaintext[offset : offset + block_size]
        xored = bytes(a ^ b for a, b in zip(block, previous))
        encrypted = _encrypt_block(xored, expanded_key)
        ciphertext.extend(encrypted)
        previous = encrypted
    return bytes(ciphertext)


def _write_preference_file(directory, payload):
    """Write *payload* as an encrypted preference file, return its path."""
    plaintext = json.dumps(payload).encode("utf-8")
    ciphertext = _encrypt_preference(plaintext)
    encoded = base64.b64encode(ciphertext).decode("ascii")
    path = pathlib.Path(directory) / "Preference.encyrpted"
    path.write_text(encoded + "\n", encoding="utf-8-sig")
    return path


class TestGetCachedLogin(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self.directory = pathlib.Path(self._temp_dir.name)
        self.payload = {
            "Version": 1,
            "Regions": {
                "China": {
                    "Token": "T" * 32,
                    "AuthCode": "A" * 32,
                    "User": {"ID": "0" * 24, "Nickname": "test"},
                },
            },
        }

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_roundtrip_decrypt_and_read(self):
        path = _write_preference_file(self.directory, self.payload)
        self.assertEqual(quantum_physics.get_cached_login(path), ("T" * 32, "A" * 32))

    def test_wrong_region(self):
        path = _write_preference_file(self.directory, self.payload)
        with self.assertRaisesRegex(ValueError, "region"):
            quantum_physics.get_cached_login(path, "US")

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            quantum_physics.get_cached_login(self.directory / "Preference.encyrpted")

    def test_damaged_file(self):
        path = _write_preference_file(self.directory, self.payload)
        path.write_text("not base64!", encoding="utf-8-sig")
        with self.assertRaises(ValueError):
            quantum_physics.get_cached_login(path)

    def test_missing_credentials(self):
        payload = {"Regions": {"China": {}}}
        path = _write_preference_file(self.directory, payload)
        with self.assertRaisesRegex(ValueError, "Token"):
            quantum_physics.get_cached_login(path)

    def test_invalid_region_type(self):
        path = _write_preference_file(self.directory, self.payload)
        with self.assertRaises(TypeError):
            quantum_physics.get_cached_login(path, region=42)


class TestPreferenceLogin(unittest.TestCase):
    @mock.patch("physicslab.web.api.token_login", return_value="logged-in-user")
    @mock.patch(
        "physicslab.quantum_physics.get_cached_login",
        return_value=("cached-token", "cached-auth-code"),
    )
    def test_login_delegates_to_token_login(
        self, mocked_get_cached_login, mocked_token_login
    ):
        path = pathlib.Path("C:/games/Quantum Physics/Preference.encyrpted")
        result = web.preference_login(path, region="China", domain="example.com")

        mocked_get_cached_login.assert_called_once_with(path, "China")
        mocked_token_login.assert_called_once_with(
            "cached-token", "cached-auth-code", "example.com"
        )
        self.assertEqual(result, "logged-in-user")

    def test_invalid_argument_types(self):
        with self.assertRaises(TypeError):
            web.preference_login("C:/games/Quantum Physics/Preference.encyrpted")
        with self.assertRaises(TypeError):
            web.preference_login(
                pathlib.Path("C:/path/Preference.encyrpted"), region=42
            )


class TestAsyncPreferenceLogin(unittest.IsolatedAsyncioTestCase):
    @mock.patch("physicslab.web.api.token_login", return_value="logged-in-user")
    @mock.patch(
        "physicslab.quantum_physics.get_cached_login",
        return_value=("cached-token", "cached-auth-code"),
    )
    async def test_async_login_delegates_to_token_login(
        self, mocked_get_cached_login, mocked_token_login
    ):
        path = pathlib.Path("C:/games/Quantum Physics/Preference.encyrpted")
        result = await web.async_preference_login(path, "China", "example.com")

        mocked_get_cached_login.assert_called_once_with(path, "China")
        mocked_token_login.assert_called_once_with(
            "cached-token", "cached-auth-code", "example.com"
        )
        self.assertEqual(result, "logged-in-user")


if __name__ == "__main__":
    unittest.main()
