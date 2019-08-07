import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user("testjust", "testing@test.com")
        self.assertTrue(user.id)
        self.assertEqual(user.username, "testjust")
        self.assertEqual(user.email, "testing@test.com")
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user("testjust", "testing@test.com")
        duplicate_user = User(username="testjust", email="testing@test2.com")
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user("testjust", "testing@test.com")
        duplicate_user = User(username="newuser", email="testing@test.com")
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user("testjust", "testing@test.com")
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))


if __name__ == "__main__":
    unittest.main()
