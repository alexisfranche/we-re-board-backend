from lettuce import *
import urllib, json
import requests

from requests.auth import HTTPDigestAuth

## STEP DEFINITIONS



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
    world.email = -1
    
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
@step('I am logged in the application as an user with id = (\d+) and email = "([^"]*)"')
def given_i_am_logged_in_the_application(step, user_id, user_email):
    world.user_id = user_id
    world.user_email = user_email
    
@step('I enter a new name "([^"]*)"')
def given_i_enter_a_new_name_group1(step, group1):
    world.newname = group1
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/profile/"+str(world.user_id))
    if 'error' in result:
        world.error = result
        return error
    else:
        world.myoldprofile = result
        url = "https://were-board.herokuapp.com/user/profile/name/"+str(world.user_email)
        world.mynewprofile = putJSONtoAPI(url, {"name":group1})
    
@step('the system displays my new name on my profile page')
def then_the_system_displays_my_new_name_on_my_profile_page(step):
    assert str(world.mynewprofile["id"]) == str(world.myoldprofile), \
        "Got id = %s instead of %s" % (world.mynewprofile["id"], world.myoldprofile)
        
    assert world.mynewprofile["name"] == step.hashes[0]["Name"], \
         "Got name = %s instead of %s" % (world.mynewprofile["name"], world.newname)
         
    assert world.mynewprofile["email"] == world.myoldprofile["email"], \
         "Got email = %s instead of %s" % (world.mynewprofile["email"], world.myoldprofile["email"]) 
         
    assert world.mynewprofile["description"] == world.myoldprofile["description"], \
         "Got description = %s instead of %s" % (world.mynewprofile["description"], world.myoldprofile["description"])
  
    assert world.mynewprofile["password"] == world.myoldprofile["password"], \
         "Got password = %s instead of %s" % (world.myprofile["password"], world.myoldprofile["password"])
         
    #reset user to original state
    url = "https://were-board.herokuapp.com/user/profile/name/"+str(world.user_email)
    response = putJSONtoAPI(url, {"name":world.myoldprofile["name"]})
    
@step('I enter a new password "([^"]*)"')
def when_i_enter_a_new_password_group1(step, group1):
    assert False, 'This step must be implemented'
@step('the system saves my new password')
def then_the_system_saves_my_new_password(step):
    assert False, 'This step must be implemented'
@step('I enter a new email "([^"]*)"')
def when_i_enter_a_new_email_group1(step, group1):
    assert False, 'This step must be implemented'
@step('The system saves my email')
def then_the_system_saves_my_email(step):
    assert False, 'This step must be implemented'
@step('I change my profile description to "([^"]*)"')
def when_i_change_my_profile_description_to_group1(step, group1):
    assert False, 'This step must be implemented'
@step('The system saves my new profile description')
def then_the_system_saves_my_new_profile_description(step):
    assert False, 'This step must be implemented'
@step('I enter a new invalid password "([^"]*)"')
def when_i_enter_a_new_invalid_password_group1(step, group1):
    assert False, 'This step must be implemented'
@step('I should receive an error message')
def then_i_should_receive_an_error_message(step):
    assert False, 'This step must be implemented'
# ID_010 View selected user profile


@step('When I view a user\'s profile with id (\d+)')
def view_user_profile(step, viewed_user_id):
    world.viewed_user_id = viewed_user_id
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/" + str(world.viewed_user_id))
    if 'error' in result:
        world.error = result
    else:
        world.viewed_user = result


      
##HELPER FUCNTIONS
def getJSONfromAPI(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data
def getJSONfromLoginAPI(name, password):
    url = "https://were-board.herokuapp.com/login"
    data = { "name": name, "password": password }
    response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    print(response)
    return response
    
def putJSONtoAPI(url, data):
    payload = data
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, data = payload)
    return response
