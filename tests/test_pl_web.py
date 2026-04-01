import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARY_DIR = os.path.dirname(SCRIPT_DIR)

import sys

sys.path.append(SCRIPT_DIR)
sys.path.append(LIBRARY_DIR)

import unittest
import _user
from datetime import datetime
from physicslab import web, Tag, Category, GetUserMode


class TestWebApi(unittest.IsolatedAsyncioTestCase):
    @staticmethod
    async def test_get_start_page():
        await web.async_get_start_page()

    async def test_get_avatar(self):
        await web.async_get_avatar(
            target_id="5ce629e157035932b52f9315",
            index=1,
            category="users",
            size_category="small.round",
        )

    async def test_get_library(self):
        await _user.user.async_get_library()

    async def test_query_experiments(self):
        await _user.user.async_query_experiments(
            tags=[Tag.Featured], category=Category.Experiment
        )

    async def test_get_experiment(self):
        await _user.user.async_get_experiment(
            content_id="6317fabebfd18200013c710c", category=Category.Experiment
        )

    async def test_get_comments(self):
        await _user.user.async_get_comments(
            target_id="6317fabebfd18200013c710c", target_type="Experiment"
        )

    async def test_get_summary(self):
        await _user.user.async_get_summary(
            content_id="6317fabebfd18200013c710c", category=Category.Experiment
        )

    async def test_get_derivatives(self):
        await _user.user.async_get_derivatives(
            content_id="6317fabebfd18200013c710c", category=Category.Experiment
        )

    async def test_get_user(self):
        await _user.user.async_get_user("5ce629e157035932b52f9315", GetUserMode.by_id)

    async def test_get_profile(self):
        await _user.user.async_get_profile()

    async def test_notifications_msg_iter(self):
        counter = 0
        start_timestamp = datetime(2025, 1, 1).timestamp() * 1000
        end_timestamp = datetime(2025, 1, 2).timestamp() * 1000
        for msg in web.NotificationsIter(_user.user, max_retry=2, category_id=5):
            if start_timestamp <= msg["Timestamp"] < end_timestamp:
                counter += 1
            elif start_timestamp > msg["Timestamp"]:
                break
        self.assertEqual(counter, 96)

    async def test_banned_msg_iter(self):
        counter = 0
        for _ in web.BannedMsgIter(
            _user.user,
            start_time=datetime(2025, 1, 1).timestamp(),
            end_time=datetime(2025, 1, 16).timestamp(),
            max_retry=4,
        ):
            counter += 1
        self.assertEqual(counter, 1)

    async def test_comments_iter(self):
        for _ in web.CommentsIter(
            _user.user, content_id="677d5c6c826568de4e9896c5", category="Discussion"
        ):
            pass

    # temp user can't get comments on _user.user's profile
    # async def test_warned_msg_iter(self):
    #     counter = 0
    #     for _ in web.WarnedMsgIter(user=user, _user.user_id="63e76ce5fd0015cb932e8b05", start_time=1731155184, end_time=1731155185):
    #         counter += 1
    #     self.assertEqual(counter, 1)

    async def test_relations_iter(self):
        for _ in web.RelationsIter(
            _user.user,
            user_id="62d3fd092f3a2a60cc8ccc9e",
            display_type="Following",
            max_retry=4,
        ):
            pass

    async def test_avatars_iter(self):
        for _ in web.AvatarsIter(
            _user.user,
            target_id="5ce629e157035932b52f9315",
            category="User",
            size_category="small.round",
            max_retry=4,
        ):
            pass

    async def test_experiments_iter(self):
        counter = 0
        start_timestamp = datetime(2025, 1, 1).timestamp() * 1000
        end_timestamp = datetime(2025, 1, 2).timestamp() * 1000
        for msg in web.ExperimentsIter(
            _user.user, category=Category.Experiment, max_retry=3
        ):
            if start_timestamp <= msg["CreationDate"] < end_timestamp:
                counter += 1
            elif start_timestamp > msg["CreationDate"]:
                break
        self.assertEqual(counter, 2)


if __name__ == "__main__":
    unittest.main()
