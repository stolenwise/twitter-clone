"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql://lewis.stone:R3dr0ver#897@localhost/warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

with app.app_context():
    db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    @classmethod
    def setUpClass(cls):
        """Set up once for the whole class."""
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.drop_all()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up context."""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Create test client, add sample data."""
        self.client = app.test_client()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def test_user_repr(self):
        """Does the repr method work as expected?"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(repr(u), f"<User #{u.id}: {u.username}, {u.email}>")

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        u1.following.append(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))
        self.assertFalse(u1.is_following(u1))
        self.assertFalse(u2.is_following(u2))
        self.assertFalse(u1.is_following(None))
        self.assertFalse(u2.is_following(None))


    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        u1.followers.append(u2)
        db.session.commit()
        self.assertTrue(u1.is_followed_by(u2))
        self.assertFalse(u2.is_followed_by(u1))
        self.assertFalse(u1.is_followed_by(u1))
        self.assertFalse(u2.is_followed_by(u2))     

    def test_user_signup(self):
        """Does User.signup successfully create a new user given valid credentials?"""
        u = User.signup(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD",
            image_url=None
        )
        db.session.commit()
        self.assertIsNotNone(u)
        self.assertEqual(u.username, "testuser")
        self.assertEqual(u.email, "test@test.com")
        self.assertNotEqual(u.password, "HASHED_PASSWORD")
        self.assertIsNotNone(u.password)

    def test_user_signup_invalid_username(self):
        """Does User.signup fail to create a new user if username is invalid?"""

        with self.assertRaises(ValueError):
            User.signup(
                username=None,
                email="test@test.com",
                password="HASHED_PASSWORD",
                image_url=None
            )

        db.session.rollback()

        # There should be no users in the database after rollback
        users = User.query.all()
        self.assertEqual(len(users), 0)

    def test_user_authenticate_valid(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""
        u = User.signup(
            username="testuser",
            email="test@test.com",
            password="password123",
            image_url=None
        )
        db.session.commit()
        authenticated_user = User.authenticate("testuser", "password123")
        self.assertIsNotNone(authenticated_user)   
        self.assertEqual(authenticated_user.username, "testuser")
        self.assertEqual(u.id, authenticated_user.id)



    def test_user_authenticate_invalid_username(self):
        """Fails to return a user when the username is invalid"""
        User.signup(
            username="testuser",
            email="test@test.com",
            password="password123",
            image_url=None
        )
        db.session.commit()

        self.assertFalse(User.authenticate("wronguser", "password123"))

    def test_user_authenticate_invalid_password(self):
        """Fails to return a user when the password is invalid"""
        User.signup(
            username="testuser",
            email="test@test.com",
            password="password123",
            image_url=None
        )
        db.session.commit()
        self.assertFalse(User.authenticate("testuser", "wrongpassword"))

    


if __name__ == '__main__':
    import unittest
    unittest.main()
