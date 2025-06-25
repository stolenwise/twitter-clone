"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import app, db
from models import User, Message, Follows

with app.app_context():
    # Reset database
    db.drop_all()
    db.create_all()

    # Load from CSVs
    with open('generator/users.csv') as users:
        db.session.bulk_insert_mappings(User, DictReader(users))

    with open('generator/messages.csv') as messages:
        db.session.bulk_insert_mappings(Message, DictReader(messages))

    with open('generator/follows.csv') as follows:
        db.session.bulk_insert_mappings(Follows, DictReader(follows))

    # Add example data manually
    u1 = User.signup(username="testuser1", email="test1@test.com", password="password", image_url=None)
    u2 = User.signup(username="testuser2", email="test2@test.com", password="password", image_url=None)

    db.session.add_all([u1, u2])
    db.session.commit()

    print("🌱 Database seeded from CSV + sample users added.")
