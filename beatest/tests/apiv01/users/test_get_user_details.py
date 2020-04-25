import unittest

from wsgi import app
from extensions import db
from models import User


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.app_context().push()
        user = User(email="gooozmago@gmail.com")
        db.session.add(user)
        db.session.flush()

    def test_main_page(self):
        response = self.app.get('/api/v0.1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        print(User.query.filter(User.email == "gooozmago@gmail.com").all())
