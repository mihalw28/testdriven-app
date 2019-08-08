import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user("testjust", "testing@test.com", "randomrandom")
        self.assertTrue(user.id)
        self.assertEqual(user.username, "testjust")
        self.assertEqual(user.email, "testing@test.com")
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        add_user("testjust", "testing@test.com", "randomrandom")
        duplicate_user = User(
            username="testjust",
            email="testing@test2.com",
            password="randomrandom",
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user("testjust", "testing@test.com", "randomrandom")
        duplicate_user = User(
            username="newuser",
            email="testing@test.com",
            password="randomrandom",
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user("testjust", "testing@test.com", "randomrandom")
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user("testjust", "test@testing.com", "randomrandom")
        user_two = add_user("testjust2", "test@testing2.com", "randomrandom")
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user("testjust", "test@testing.com", "randomrandom")
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user("testjust", "test@testing.com", "randomrandom")
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_auth_token(auth_token), user.id)


if __name__ == "__main__":
    unittest.main()
