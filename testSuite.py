from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        self.assertIn(b'You were logged in.', response.data)

    # Ensure signup behaves correctly with correct credentials
    def test_correct_signup(self):
        tester = app.test_client()
        response = tester.get('/user')
        try:
            self.assertIn(b'"email": "admin@gmail.ca"', response.data)
        except AssertionError:
            response = tester.post('/user',
                                   json=dict(name="admin", email="admin@gmail.ca", password="adminPassword#123"))
            self.assertIn(b'"email": "admin@gmail.ca"', response.data)

        self.assertEqual(response.status_code, 200)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client()
        response = tester.post('/login', json=dict(email="wrong@mail.com", password="wrong"))
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client()
        # tester.post('/login', json=dict(email="admin", password="admin"))
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out.', response.data)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        tester = app.test_client()
        response = tester.get('/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    # Ensure that event behaves correctly
    def test_event(self):
        tester = app.test_client()
        response = tester.post('/event',
                               json=dict(name="Anas", address="101 Game Street, Montreal", game="Texas Hold Em",
                                         datetime="2020-03-08 09:05:06", description="Work hard, Play hard",
                                         event_manager_id="1")
                               )
        self.assertEqual(response.status_code, 200)
        response = tester.get('/event')
        self.assertIn(
            b'"address": "101 Game Street, Montreal", \n    "datetime": "2020-03-08T09:05:06+00:00", \n    "description": "Work hard, Play hard", \n    "event_manager_id": 1, \n    "game": "Texas Hold Em"',
            response.data)


if __name__ == '__main__':
    unittest.main()
