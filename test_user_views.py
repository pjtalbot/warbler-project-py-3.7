import os
from unittest import TestCase
from sqlalchemy import exc
import pdb
from bs4 import BeautifulSoup

from models import db, User, Message, Follows


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()


        u1 = User.signup("user_test_1", 'ut1@gmail.com', '12345', None)
        u1_id = 500
        u1.id = u1_id

        u2 = User.signup('user_test_2', 'ut2@gmail.com', '54321', None)
        u2_id = 600
        u2.id = u2_id

        # db.session.add_all([u1, u2])
        db.session.commit()

        u1 = User.query.get(u1_id)
        u2 = User.query.get(u2.id)

        self.u1 = u1
        self.u2 = u2

        self.client = app.test_client()
    def tearDown(self):
       
        res = super().tearDown()
        db.session.rollback()
        return res

    def setUp_messages(self):
        m1 = Message(text="testing123", user_id=self.u1.id)
        m2 = Message(text="456testing", user_id=self.u2.id)
        m3 = Message(id=9876, text="8910testtest", user_id=self.u1.id)

        db.session.add_all([m1, m2, m3])
        db.session.commit()

    def test_users_list(self):
        with self.client as c:
            resp = c.get(f'/users')
            

            self.assertIn("user_test_1", str(resp.data))
            self.assertIn("user_test_2", str(resp.data))
           
            # self.assertNotIn("user_test_3", str(resp.data))
            # self.assertIn('/users/600', str(resp.data))

    def test_user_profile_view(self):
        with self.client as c:
            resp = c.get(f'/users/600')
            # pdb.set_trace()
            self.assertEqual(resp.status_code, 200)

            self.assertIn('<a href="/users/600/following">0</a>', str(resp.data))

    
    


            # self.assertIn()
    def test_likes(self):
        self.setUp_messages()

        with self.client as c:
            resp = c.get(f'/users/500')

            self.assertEqual(resp.status_code, 200)
            pdb.set_trace()

            # Beautfiful Soup, very cool!

            self.assertIn('<a href="/messages/1"', str(resp.data))
            soup = BeautifulSoup(str(resp.data), 'html.parser')
            found = soup.select('a[href="/users/500"]')

            



