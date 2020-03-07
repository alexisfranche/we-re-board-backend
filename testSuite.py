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

    # Ensure that access event behaves correctly
    def test_correct_access_event(self):
        tester = app.test_client()
        data = {"name":"Antonios", "address":"2345 Rue life ouest", "game":"board game night","datetime":"2020-04-08 07:09:01", "description":"all kinds of board games to play", "event_manager_id":'2'}
        event = tester.post('/event', json=data)
        response = tester.get('/event/'+ str(event.json['id']), follow_redirects=True)
        self.assertEquals(response.status_code, 200)

    # Ensure that access event behaves incorrectly 
    def test_incorrect_access_event(self):
        tester = app.test_client()
        response = tester.get('/event/54367', follow_redirects=True)
        self.assertEquals(response.status_code, 404)

    # ensure is event user behaves correctly 
    def test_correct_is_event_user(self):
        tester = app.test_client()
        event_data = {"name":"Antonios", "address":"2345 Rue life ouest", "game":"board game night","datetime":"2020-04-08 07:09:01", "description":"all kinds of board games to play", "event_manager_id":'2'}
        user_data = {"name":"Antonios7", "email":"Antonios7@gmail.com", "password":"7832748#HGkjhdawH"}

        event = tester.post('/event', json=event_data)
        user = tester.post('/user', json=user_data)
        print("EVENT*7897873428729837423:"+str(user.json))
        event_user_data = {"event_id":event.json['id'], "user_id":user.json['id']}
        event_user = tester.post('/join', json=event_user_data)

        response = tester.post('/event_user/exists', json= event_user_data)


        tester.delete('/user/'+str(user.json['id']))
        self.assertEqual(response.json['is_joined'], True)

    #ensure is event user behaves icorrectly
    def test_incorrect_is_event_user(self):
        tester = app.test_client()
        event_user_data = {"event_id":87654, "user_id":"98765"}
        response = tester.post('/event_user/exists', json=event_user_data)
        self.assertEqual(response.json['is_joined'], False)






if __name__ == '__main__':
    unittest.main()