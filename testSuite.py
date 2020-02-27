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

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        tester = app.test_client()
        #response = tester.post('/login', data=dict(email="admin", password="admin"), follow_redirects=True)
        #self.assertIn(response.status_code, 200)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client()
        #response = tester.post('/login',
        #                        data=dict(email="wrong@mail.com", password="wrong"),
        #                        follow_redirects=True
        #                        )
        #self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client()
        #tester.post('/login',
        #         data=dict(email="admin", password="admin"),
        #         follow_redirects=True
        #         )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out.', response.data)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        tester = app.test_client()
        response = tester.get('/', follow_redirects=True)
        self.assertIn(b'were board backend!!! </h1> You need to login first.', response.data)

    # Ensure that logout page requires user login
    def test_logout_route_requires_login(self):
         tester = app.test_client()
        # response = tester.get('/logout', follow_redirects=True)
        # self.assertIn(b'You need to login first.', response.data)

if __name__ == '__main__':
    unittest.main()