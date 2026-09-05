"""Quantum-Physics utilities for the physicslab package.

This module reads the local data of the Quantum-Physics app (e.g. its version
and the cloud login credentials cached in its encrypted preference file).
"""

import base64
import json
import os
import pathlib
import platform

from typing import Optional, Tuple


_CACHE_PASSWORD_HEX = "14D9696C49D24F87"
_BLOCK_SIZE = 16
_PREFERENCE_FILENAME = "Preference.encyrpted"

_RIJNDAEL_BLOCK_WORDS = _BLOCK_SIZE // 4
_RIJNDAEL_KEY_WORDS = 2
_RIJNDAEL_ROUNDS = 10
_EXPANDED_KEY_WORDS = _RIJNDAEL_BLOCK_WORDS * (_RIJNDAEL_ROUNDS + 1)


# Standard Rijndael S-box.  The preference file uses a 128-bit block but a
# nonstandard 64-bit key (Nk=2); the round transform itself is the regular
# Rijndael one.
_SBOX = (
    0x63,
    0x7C,
    0x77,
    0x7B,
    0xF2,
    0x6B,
    0x6F,
    0xC5,
    0x30,
    0x01,
    0x67,
    0x2B,
    0xFE,
    0xD7,
    0xAB,
    0x76,
    0xCA,
    0x82,
    0xC9,
    0x7D,
    0xFA,
    0x59,
    0x47,
    0xF0,
    0xAD,
    0xD4,
    0xA2,
    0xAF,
    0x9C,
    0xA4,
    0x72,
    0xC0,
    0xB7,
    0xFD,
    0x93,
    0x26,
    0x36,
    0x3F,
    0xF7,
    0xCC,
    0x34,
    0xA5,
    0xE5,
    0xF1,
    0x71,
    0xD8,
    0x31,
    0x15,
    0x04,
    0xC7,
    0x23,
    0xC3,
    0x18,
    0x96,
    0x05,
    0x9A,
    0x07,
    0x12,
    0x80,
    0xE2,
    0xEB,
    0x27,
    0xB2,
    0x75,
    0x09,
    0x83,
    0x2C,
    0x1A,
    0x1B,
    0x6E,
    0x5A,
    0xA0,
    0x52,
    0x3B,
    0xD6,
    0xB3,
    0x29,
    0xE3,
    0x2F,
    0x84,
    0x53,
    0xD1,
    0x00,
    0xED,
    0x20,
    0xFC,
    0xB1,
    0x5B,
    0x6A,
    0xCB,
    0xBE,
    0x39,
    0x4A,
    0x4C,
    0x58,
    0xCF,
    0xD0,
    0xEF,
    0xAA,
    0xFB,
    0x43,
    0x4D,
    0x33,
    0x85,
    0x45,
    0xF9,
    0x02,
    0x7F,
    0x50,
    0x3C,
    0x9F,
    0xA8,
    0x51,
    0xA3,
    0x40,
    0x8F,
    0x92,
    0x9D,
    0x38,
    0xF5,
    0xBC,
    0xB6,
    0xDA,
    0x21,
    0x10,
    0xFF,
    0xF3,
    0xD2,
    0xCD,
    0x0C,
    0x13,
    0xEC,
    0x5F,
    0x97,
    0x44,
    0x17,
    0xC4,
    0xA7,
    0x7E,
    0x3D,
    0x64,
    0x5D,
    0x19,
    0x73,
    0x60,
    0x81,
    0x4F,
    0xDC,
    0x22,
    0x2A,
    0x90,
    0x88,
    0x46,
    0xEE,
    0xB8,
    0x14,
    0xDE,
    0x5E,
    0x0B,
    0xDB,
    0xE0,
    0x32,
    0x3A,
    0x0A,
    0x49,
    0x06,
    0x24,
    0x5C,
    0xC2,
    0xD3,
    0xAC,
    0x62,
    0x91,
    0x95,
    0xE4,
    0x79,
    0xE7,
    0xC8,
    0x37,
    0x6D,
    0x8D,
    0xD5,
    0x4E,
    0xA9,
    0x6C,
    0x56,
    0xF4,
    0xEA,
    0x65,
    0x7A,
    0xAE,
    0x08,
    0xBA,
    0x78,
    0x25,
    0x2E,
    0x1C,
    0xA6,
    0xB4,
    0xC6,
    0xE8,
    0xDD,
    0x74,
    0x1F,
    0x4B,
    0xBD,
    0x8B,
    0x8A,
    0x70,
    0x3E,
    0xB5,
    0x66,
    0x48,
    0x03,
    0xF6,
    0x0E,
    0x61,
    0x35,
    0x57,
    0xB9,
    0x86,
    0xC1,
    0x1D,
    0x9E,
    0xE1,
    0xF8,
    0x98,
    0x11,
    0x69,
    0xD9,
    0x8E,
    0x94,
    0x9B,
    0x1E,
    0x87,
    0xE9,
    0xCE,
    0x55,
    0x28,
    0xDF,
    0x8C,
    0xA1,
    0x89,
    0x0D,
    0xBF,
    0xE6,
    0x42,
    0x68,
    0x41,
    0x99,
    0x2D,
    0x0F,
    0xB0,
    0x54,
    0xBB,
    0x16,
)

_INV_SBOX = bytes.maketrans(bytes(_SBOX), bytes(range(256)))


def get_quantum_physics_version() -> Optional[Tuple[int, int, int]]:
    """Get version of Quantum-Physics, return None if failed to get version."""
    if platform.system() != "Windows":
        return None

    from physicslab.constant import WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR

    try:
        a_dir = os.listdir(
            os.path.join(WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR, "Unity")
        )
        if len(a_dir) != 1:
            return None

        a_file = os.path.join(
            WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR,
            "Unity",
            a_dir[0],
            "Analytics",
            "values",
        )

        with open(a_file) as f:
            ver_str: str = json.load(f)["app_ver"]
        parts = ver_str.split(".")
        if len(parts) != 3:
            return None
        major, minor, patch = parts
        return int(major), int(minor), int(patch)
    except json.decoder.JSONDecodeError, UnicodeDecodeError, FileNotFoundError:
        return None
    except ValueError:
        return None


def get_quantum_physics_path() -> Optional[str]:
    """Get path of Quantum-Physics."""
    if platform.system() != "Windows":
        return None

    from physicslab.constant import WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR

    with open(
        os.path.join(WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR, "Player-prev.log")
    ) as f:
        f.readline()
        f.readline()
        res = os.path.dirname(os.path.dirname(f.readline()[25:-2]))

    if res == "":
        return None
    return res


def get_preference_path() -> Optional[pathlib.Path]:
    """Get path of Quantum-Physics's encrypted preference file.

    Returns:
        The path of the encrypted preference file if the platform is Windows,
        otherwise None.

    """
    if platform.system() != "Windows":
        return None

    from physicslab.constant import WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR

    return pathlib.Path(WIN_QUANTAM_PHYSICS_STORAGE_STRING_DIR) / _PREFERENCE_FILENAME


def get_cached_login(
    preference_path: pathlib.Path,
    region: str = "China",
) -> Tuple[str, str]:
    """Get the cloud login credentials cached by Quantum-Physics.

    The Quantum-Physics app caches the login credentials of the CIVITAS cloud
    account in its encrypted preference file. The credentials of the account
    bound to *region* are returned.

    Args:
        preference_path: Path of the encrypted preference file.
        region: The region of the account, e.g. "China" or "US".

    Returns:
        A tuple of ``(token, auth_code)`` of the cached account.

    Raises:
        FileNotFoundError: The preference file does not exist.
        ValueError: The preference file is damaged, the *region* account is not
            bound, or the cached credentials are invalid.

    """
    if not isinstance(region, str):
        raise TypeError(
            f"Parameter `region` must be of type `str`, but got value `{region}` of type `{type(region).__name__}`"
        )

    data = json.loads(_decrypt_preference_file(preference_path))

    if isinstance(data, dict) and isinstance(data.get("Regions"), dict):
        region_data = data["Regions"].get(region)
    else:
        region_data = None
    if not isinstance(region_data, dict):
        raise ValueError(
            f"Quantum-Physics preference file has no cached login for region {region!r}"
        )

    token = region_data.get("Token")
    auth_code = region_data.get("AuthCode")
    if not isinstance(token, str) or not token:
        raise ValueError(
            f"Quantum-Physics preference file has no valid Token for region {region!r}"
        )
    if not isinstance(auth_code, str) or not auth_code:
        raise ValueError(
            f"Quantum-Physics preference file has no valid AuthCode for region {region!r}"
        )
    return token, auth_code


def _xtime(value: int) -> int:
    """Multiply one byte by x in GF(2^8), modulo x^8+x^4+x^3+x+1."""

    return ((value << 1) ^ (0x11B if value & 0x80 else 0)) & 0xFF


def _gf_multiply(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        left = _xtime(left)
        right >>= 1
    return result


_MUL_9 = tuple(_gf_multiply(value, 9) for value in range(256))
_MUL_11 = tuple(_gf_multiply(value, 11) for value in range(256))
_MUL_13 = tuple(_gf_multiply(value, 13) for value in range(256))
_MUL_14 = tuple(_gf_multiply(value, 14) for value in range(256))

# Source indexes for inverse ShiftRows in Rijndael's column-major state.
_INV_SHIFT_ROWS = (0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3)


def _rot_word(word: int) -> int:
    return ((word << 8) & 0xFFFFFFFF) | (word >> 24)


def _sub_word(word: int) -> int:
    return (
        (_SBOX[(word >> 24) & 0xFF] << 24)
        | (_SBOX[(word >> 16) & 0xFF] << 16)
        | (_SBOX[(word >> 8) & 0xFF] << 8)
        | _SBOX[word & 0xFF]
    )


def _expand_game_key(key: bytes) -> bytes:
    """Expand the game's nonstandard 64-bit Rijndael key."""

    words = [
        int.from_bytes(key[offset : offset + 4], "big")
        for offset in range(0, len(key), 4)
    ]

    rcon = 0x01
    for index in range(_RIJNDAEL_KEY_WORDS, _EXPANDED_KEY_WORDS):
        temp = words[index - 1]
        if index % _RIJNDAEL_KEY_WORDS == 0:
            temp = _sub_word(_rot_word(temp)) ^ (rcon << 24)
            rcon = _xtime(rcon)
        words.append((words[index - _RIJNDAEL_KEY_WORDS] ^ temp) & 0xFFFFFFFF)

    return b"".join(word.to_bytes(4, "big") for word in words)


def _add_round_key(state: list, expanded_key: bytes, round_index: int) -> None:
    offset = round_index * _BLOCK_SIZE
    for index in range(_BLOCK_SIZE):
        state[index] ^= expanded_key[offset + index]


def _inverse_sub_shift_rows(state: list) -> list:
    """Apply inverse ShiftRows and inverse SubBytes in one permutation."""

    return [_INV_SBOX[state[index]] for index in _INV_SHIFT_ROWS]


def _inverse_mix_columns(state: list) -> None:
    for column in range(4):
        offset = 4 * column
        a0 = state[offset]
        a1 = state[offset + 1]
        a2 = state[offset + 2]
        a3 = state[offset + 3]
        state[offset] = _MUL_14[a0] ^ _MUL_11[a1] ^ _MUL_13[a2] ^ _MUL_9[a3]
        state[offset + 1] = _MUL_9[a0] ^ _MUL_14[a1] ^ _MUL_11[a2] ^ _MUL_13[a3]
        state[offset + 2] = _MUL_13[a0] ^ _MUL_9[a1] ^ _MUL_14[a2] ^ _MUL_11[a3]
        state[offset + 3] = _MUL_11[a0] ^ _MUL_13[a1] ^ _MUL_9[a2] ^ _MUL_14[a3]


def _decrypt_block(block: bytes, expanded_key: bytes) -> bytes:
    state = list(block)
    _add_round_key(state, expanded_key, _RIJNDAEL_ROUNDS)

    for round_index in range(_RIJNDAEL_ROUNDS - 1, 0, -1):
        state = _inverse_sub_shift_rows(state)
        _add_round_key(state, expanded_key, round_index)
        _inverse_mix_columns(state)

    state = _inverse_sub_shift_rows(state)
    _add_round_key(state, expanded_key, 0)
    return bytes(state)


def _remove_pkcs7_in_place(data: bytearray) -> None:
    """Validate and remove one PKCS#7 padding suffix without copying data."""

    padding_length = data[-1]
    if not 1 <= padding_length <= _BLOCK_SIZE or not data.endswith(
        bytes([padding_length]) * padding_length
    ):
        raise ValueError(
            "invalid PKCS#7 padding (wrong key or damaged preference file)"
        )
    del data[-padding_length:]


def _decrypt_ciphertext(ciphertext: bytes) -> bytes:
    """Decrypt raw (already Base64-decoded) preference ciphertext."""

    if not ciphertext or len(ciphertext) % _BLOCK_SIZE:
        raise ValueError("ciphertext must be non-empty and a multiple of 16 bytes")

    key = bytes.fromhex(_CACHE_PASSWORD_HEX)
    # The game repeats its 8-byte cache password to form the 16-byte IV.
    iv = key + key
    expanded_key = _expand_game_key(key)

    plaintext = bytearray()
    previous = iv
    for offset in range(0, len(ciphertext), _BLOCK_SIZE):
        block = ciphertext[offset : offset + _BLOCK_SIZE]
        decrypted = _decrypt_block(block, expanded_key)
        plaintext.extend(left ^ right for left, right in zip(decrypted, previous))
        previous = block

    _remove_pkcs7_in_place(plaintext)
    return bytes(plaintext)


def _decrypt_preference_file(preference_path: pathlib.Path) -> bytes:
    """Decrypt the encrypted preference file and return its plaintext."""

    encoded = preference_path.read_text(encoding="utf-8-sig")
    ciphertext = base64.b64decode("".join(encoded.split()), validate=True)
    return _decrypt_ciphertext(ciphertext)
