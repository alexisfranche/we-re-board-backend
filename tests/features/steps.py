from lettuce import *
import urllib, json
import requests

from requests.auth import HTTPDigestAuth
 
# STEP DEFINITIONS
class User():
    def __init__( self, name, email, password):
        self.name=name
        self.email=email
        self.password=password
#ID_001 Register New User
@step('Given there is no user registered with the email \'([^\']*)\'')
def is_not_existing_user( step, email):
    result= requests.get("https://were-board.herokuapp.com/emailcheck/"+str(email))
    if (result.text=="Some"):
        user= getJSONfromAPI("https://were-board.herokuapp.com/email/"+str(email))
        requests.delete("https://were-board.herokuapp.com/email/"+str(user["id"]))
'''
@step('Given the following is an existing user:')
def is_existing_user(step):
    world.user= User(**step.hashes.first)
    requests.post("https://were-board.herokuapp.com/user", data=json.dumps({"name": world.user.name, "email":world.user.email, "password": world.user.password}), headers={"Content-Type": "application/json"})
'''        
@step('When I submit the following information to the sign-up form:')
def submit_information(step):
    world.user= User(**step.hashes.first)
    world.result= requests.post("https://were-board.herokuapp.com/user",data= json.dumps({"name": world.user.name, "email":world.user.email, "password": world.user.password}), headers={"Content-Type": "application/json"})
    
@step('Then I should be able to sign in to the app with the provided email and password')
def should_be_able_to_sign_in( step):
    response= requests.post("https://were-board.herokuapp.com/login", data=json.dumps({ "email": world.user.email, "password": world.user.password }), headers={"Content-Type": "application/json"})
    assert response.status_code==200

@step('Then the system should send an error message')
def assert_error_message( step):
    assert world.result.status_code == 400

# ID_002 Login
@step('I am already registered to the application with id = (\d+)')
def given_i_am_registered_to_the_application(step, user_id):
    world.user_id = user_id


@step('I login to the application with email = "([^"]*)" and password = "([^"]*)"')
def when_i_login_to_the_application(step, email, password):
    result = getJSONfromLoginAPI(email, password)
    if response.status_code == 401 or response.status_code == 404:
        world.error = result.error
    else:
        world.message = result.data


@step('The system logs me in and displays a confirmation message')
def then_the_system_logs_me_in_and_displays_a_confirmation_message(step):
    expected_confirmation_message = "You were logged in"
    assert world.message == expected_confirmation_message, \
        "Got message = %s instead of %s" % (world.message, expected_confirmation_message)


@step('Then the system does not log me in and displays a "([^"]*)" error message')
def then_the_system_does_not_log_me_in_and_displays_an_error_message(step, message):
    expected_error_message = message
    assert world.error == expected_error_message, \
        "Got error message = %s instead of %s" % (world.error, expected_error_message)

        
#ID_003 Logout

@step('I am logged in the application as an user with id = (\d+)')
def given_i_am_logged_in_the_application(step, user_id):
    world.user_id = user_id
    
@step('I log out of the application')
def when_i_log_out_of_the_application(step):
    result = getJSONfromAPI("https://were-board.herokuapp.com/logout")
    if 'error' in result:
        world.error = result
    else:
        world.message = result
    
@step('I should lose access to the application\'s features and redirect out')
def then_i_should_lose_access_to_the_application_s_features_and_redirect_out(step):
    expected_confirmation_message = "You were logged out"
    assert world.message["data"] == expected_confirmation_message, \
        "Got message = %s instead of %s"  % (world.message["data"], expected_confirmation_message)


#ID_004 - View Personal Profile
@step('I am logged in as an user with id = (\d+)')
def have_user_id(step, user_id):
    world.user_id = user_id
    
@step('my account does not exist')
def have_non_valid_user_id(step):
    world.user_id = -1
    
@step('I view my profile')
def view_personal_profile(step):
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/profile/"+str(world.user_id))
    if 'error' in result:
        world.error = result
    else:
        world.myprofile = result
        
@step('the system displays the following:')
def assert_personal_profile(step):

    assert str(world.myprofile["id"]) == str(step.hashes[0]["ID"]), \
        "Got id = %s instead of %s" % (world.myprofile["id"], str(step.hashes[0]["ID"]))
        
    assert world.myprofile["name"] == step.hashes[0]["Name"], \
         "Got name = %s instead of %s" % (world.myprofile["name"], str(step.hashes[0]["Name"]))
         
    assert world.myprofile["email"] == step.hashes[0]["Email"], \
         "Got email = %s instead of %s" % (world.myprofile["email"], str(step.hashes[0]["Email"])) 
         
    assert world.myprofile["description"] == step.hashes[0]["Description"], \
         "Got description = %s instead of %s" % (world.myprofile["description"], str(step.hashes[0]["Description"]))
         
    assert world.myprofile["password"] == step.hashes[0]["Password"], \
         "Got password = %s instead of %s" % (world.myprofile["password"], str(step.hashes[0]["Password"]))

@step('the system displays an "([^"]*)" error message')
def assert_error_404(step, expected):
    assert world.error["error"] == expected, \
        "Got error = %s instead of %s"  % (world.error["error"], expected)


#ID__005 - Modify Personal Profile

@step('I am logged in as an user with id = (\d+)')
def have_user_id(step, user_id, email):
    world.user_id = user_id
    world.email = email


@step('my account does not exist')
def have_non_valid_user_id(step):
    world.user_id = -1
    world.email = -1

@step('modifying my name')
def modify_name(step):
    result = getJSONfromAPI("/user/profile/name/" + str(world.email))
    if 'error' in result:
        world.error = result
    else:
        world.profile = result


@step('the system displays my new name:')
def assert_personal_profile(step):
    assert str(world.myprofile["id"]) == str(step.hashes[0]["ID"]), \
        "Got id = %s instead of %s" % (world.myprofile["id"], str(step.hashes[0]["ID"]))
    assert world.myprofile["name"] == step.hashes[0]["Name"], \
        "Got name = %s instead of %s" % (world.myprofile["name"], str(step.hashes[0]["Name"]))


@step('the system displays an "([^"]*)" error message')
def assert_error_404(step, expected):
    assert world.error["error"] == expected, \
        "Got error = %s instead of %s" % (world.error["error"], expected)


@step('modifying my password')
def modify_password(step):
    result = getJSONfromAPI("/user/profile/" + str(world.user_id))
    if 'error' in result:
        world.error = result
    else:
        world.profile = result


@step('the system displays my new password:')
def assert_personal_profile(step):
    assert str(world.myprofile["id"]) == str(step.hashes[0]["ID"]), \
        "Got id = %s instead of %s" % (world.myprofile["id"], str(step.hashes[0]["ID"]))
    assert world.myprofile["password"] == step.hashes[0]["Password"], \
        "Got password = %s instead of %s" % (world.myprofile["password"], str(step.hashes[0]["Password"]))

@step('the system displays an "([^"]*)" error message')
def assert_error_404(step, expected):
    assert world.error["error"] == expected, \
        "Got error = %s instead of %s" % (world.error["error"], expected)



@step('modifying my email')
def modify_email(step):
    result = getJSONfromAPI("/user/" + str(world.user_id))
    if 'error' in result:
        world.error = result
    else:
        world.profile = result


@step('the system displays my new email:')
def assert_personal_profile(step):
    assert str(world.myprofile["id"]) == str(step.hashes[0]["ID"]), \
        "Got id = %s instead of %s" % (world.myprofile["id"], str(step.hashes[0]["ID"]))
    assert world.myprofile["email"] == step.hashes[0]["Email"], \
        "Got email = %s instead of %s" % (world.myprofile["email"], str(step.hashes[0]["Email"]))



@step('the system displays an "([^"]*)" error message')
def assert_error_404(step, expected):
    assert world.error["error"] == expected, \
        "Got error = %s instead of %s" % (world.error["error"], expected)



@step('modifying my description')
def modify_email(step):
    result = getJSONfromAPI("/user/profile/desc/" + str(world.email))
    if 'error' in result:
        world.error = result
    else:
        world.profile = result


@step('the system displays my new description:')
def assert_personal_profile(step):
    assert str(world.myprofile["id"]) == str(step.hashes[0]["ID"]), \
        "Got id = %s instead of %s" % (world.myprofile["id"], str(step.hashes[0]["ID"]))
    assert world.myprofile["description"] == step.hashes[0]["Description"], \
        "Got description = %s instead of %s" % (world.myprofile["description"], str(step.hashes[0]["Description"]))

@step('the system displays an "([^"]*)" error message')
def assert_error_404(step, expected):
    assert world.error["error"] == expected, \
        "Got error = %s instead of %s" % (world.error["error"], expected)




##HELPER FUCNTIONS
def getJSONfromAPI(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data

def getJSONfromLoginAPI(name, password):
    url = "https://were-board.herokuapp.com/user/profile"
    data = { "name": name, "password": password }
    response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    return response