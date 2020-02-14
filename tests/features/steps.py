from lettuce import *
import urllib, json
 
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


##HELPER FUCNTIONS
def getJSONfromAPI(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data