"""User views tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
import unittest
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different
# database for tests (we need to do this
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

class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client and sample data."""
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

            self.user1 = User.signup(username="test1", email="test1@test.com", password="password", image_url=None)
            self.user2 = User.signup(username="test2", email="test2@test.com", password="password", image_url=None)
            db.session.commit()

            self.user1_id = self.user1.id
            self.user2_id = self.user2.id

    def login(self, user_id):
        """Helper to log in a user."""
        with self.client.session_transaction() as sess:
            sess["curr_user"] = user_id

    def logout(self):
        """Helper to log out."""
        return self.client.get("/logout", follow_redirects=True)

    def test_followers_page_logged_in(self):
        """Can a logged-in user see another user's followers page?"""
        with app.app_context():
            user1 = db.session.get(User, self.user1_id)
            user2 = db.session.get(User, self.user2_id)
            user2.followers.append(user1)
            db.session.commit()

            self.login(self.user1_id)

            resp = self.client.get(f"/users/{self.user2.id}/followers")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"test1", resp.data)

    def test_followers_page_logged_out(self):
        """Are logged-out users blocked from followers page?"""
        self.logout()
        resp = self.client.get(f"/users/{self.user2.id}/followers", follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Access unauthorized", resp.data)


if __name__ == "__main__":
    unittest.main()
#test_user_views.py