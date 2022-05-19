import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class MessageModelTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

       

        u1 = User.signup("user_test_1", 'ut1@gmail.com', '12345', None)
        u1_id = 500
        u1.id = u1_id

        u2 = User.signup('user_test_2', 'ut2@gmail.com', '54321', None)
        u2_id = 600
        u2.id = u2_id

       
        db.session.commit()

        u1 = User.query.get(u1_id)
        u2 = User.query.get(u2.id)

        self.u1 = u1
        self.u2 = u2

        self.client = app.test_client()
    
    def tearDown(self):
        db.session.rollback()
        return super().tearDown()

    def test_message_model(self):
        test_message = Message(text='testing123', user_id=self.u1.id)
        db.session.add(test_message)
        db.session.commit()
        self.assertEqual(self.u1.messages[0].text, "testing123")
        self.assertEqual(len(self.u1.messages), 1)
    def test_message_likes(self):
        test_message = Message(text='testing123', user_id=self.u1.id)
        db.session.add(test_message)
        db.session.commit()

        self.u2.likes.append(test_message)

        db.session.commit()

        self.assertEqual(len(self.u2.likes), 1)
        self.assertEqual(len(self.u1.likes), 0)






