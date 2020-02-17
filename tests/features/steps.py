from lettuce import *
import urllib, json
import requests
from werkzeug.security import generate_password_hash, check_password_hash
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

@step('I enter a new name "([^"]*)"')
def given_i_enter_a_new_name_group1(step, group1):
    world.newname = group1
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/profile/"+str(world.user_id))
    if 'error' in result:
        world.error = result
        return error
    else:
        world.myoldprofile = result
        url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
        data = "{\"name\":\""+group1+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\""+world.myoldprofile["password"]+"\", \"description\":\""+world.myoldprofile["description"]+"\"}"
        world.mynewprofile = putJSONtoAPI(url, data)
    
@step('the system displays my new name on my profile page')
def then_the_system_displays_my_new_name_on_my_profile_page(step):
    assert str(world.mynewprofile["id"]) == str(world.myoldprofile["id"]), \
        "Got id = %s instead of %s" % (world.mynewprofile["id"], world.myoldprofile["id"])
        
    assert world.mynewprofile["name"] == world.newname, \
         "Got name = %s instead of %s" % (world.mynewprofile["name"], world.newname)
         
    assert world.mynewprofile["email"] == world.myoldprofile["email"], \
         "Got email = %s instead of %s" % (world.mynewprofile["email"], world.myoldprofile["email"]) 
         
    assert world.mynewprofile["description"] == world.myoldprofile["description"], \
         "Got description = %s instead of %s" % (world.mynewprofile["description"], world.myoldprofile["description"])
  
         
    #reset user to original state
    url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
    data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\""+world.myoldprofile["password"]+"\", \"description\":\""+world.myoldprofile["description"]+"\"}"
    world.mynewprofile = putJSONtoAPI(url, data)
    
@step('I enter a new password "([^"]*)"')
def when_i_enter_a_new_password_group1(step, group1):
    world.newpassword = group1
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/profile/"+str(world.user_id))
    if 'error' in result:
        world.error = result
        return error
    else:
        world.myoldprofile = result
        url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
        data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\""+group1+"\", \"description\":\""+world.myoldprofile["description"]+"\"}"
        world.mynewprofile = putJSONtoAPI(url, data)
@step('the system saves my new password')
def then_the_system_saves_my_new_password(step):
    assert str(world.mynewprofile["id"]) == str(world.myoldprofile["id"]), \
        "Got id = %s instead of %s" % (world.mynewprofile["id"], world.myoldprofile["id"])
    assert world.mynewprofile["password"] != world.myoldprofile["password"], \
         "Password didn't change"
    assert world.mynewprofile["name"] == world.myoldprofile["name"], \
         "Got name = %s instead of %s" % (world.mynewprofile["name"], world.myoldprofile["name"])
         
    assert world.mynewprofile["email"] == world.myoldprofile["email"], \
         "Got email = %s instead of %s" % (world.mynewprofile["email"], world.myoldprofile["email"]) 
         
    assert world.mynewprofile["description"] == world.myoldprofile["description"], \
         "Got description = %s instead of %s" % (world.mynewprofile["description"], world.myoldprofile["description"])
  
         
    #reset user to original state
    url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
    data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\""+world.myoldprofile["password"]+"\", \"description\":\""+world.myoldprofile["description"]+"\"}"
    world.mynewprofile = putJSONtoAPI(url, data)
    
@step('I enter a new email "([^"]*)"')
def when_i_enter_a_new_email_group1(step, group1):
    world.newemail = group1
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/profile/"+str(world.user_id))
    if 'error' in result:
        world.error = result
        return error
    else:
        world.myoldprofile = result
        url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
        data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+group1+"\", \"password\":\""+world.myoldprofile["password"]+"\", \"description\":\""+world.myoldprofile["description"]+"\"}"
        world.mynewprofile = putJSONtoAPI(url, data)
@step('The system saves my email')
def then_the_system_saves_my_email(step):
    assert str(world.mynewprofile["id"]) == str(world.myoldprofile["id"]), \
        "Got id = %s instead of %s" % (world.mynewprofile["id"], world.myoldprofile["id"])
  
    assert world.mynewprofile["name"] == world.myoldprofile["name"], \
         "Got name = %s instead of %s" % (world.mynewprofile["name"], world.myoldprofile["name"])
         
    assert world.mynewprofile["email"] == world.newemail, \
         "Got email = %s instead of %s" % (world.mynewprofile["email"], world.newemail) 
         
    assert world.mynewprofile["description"] == world.myoldprofile["description"], \
         "Got description = %s instead of %s" % (world.mynewprofile["description"], world.myoldprofile["description"])
  
         
    #reset user to original state
    url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
    data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\""+world.myoldprofile["password"]+"\", \"description\":\""+world.myoldprofile["description"]+"\"}"
    world.mynewprofile = putJSONtoAPI(url, data)

@step('I change my profile description to "([^"]*)"')
def when_i_change_my_profile_description_to_group1(step, group1):
    world.newdescription = group1
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/profile/"+str(world.user_id))
    if 'error' in result:
        world.error = result
        return error
    else:
        world.myoldprofile = result
        url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
        data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\""+world.myoldprofile["password"]+"\", \"description\":\""+group1+"\"}"
        world.mynewprofile = putJSONtoAPI(url, data)
@step('The system saves my new profile description')
def then_the_system_saves_my_new_profile_description(step):
    assert str(world.mynewprofile["id"]) == str(world.myoldprofile["id"]), \
        "Got id = %s instead of %s" % (world.mynewprofile["id"], world.myoldprofile["id"])
  
    assert world.mynewprofile["name"] == world.myoldprofile["name"], \
         "Got name = %s instead of %s" % (world.mynewprofile["name"], world.myoldprofile["name"])
         
    assert world.mynewprofile["email"] == world.myoldprofile["email"], \
         "Got email = %s instead of %s" % (world.mynewprofile["email"], world.myoldprofile["email"]) 
         
    assert world.mynewprofile["description"] == world.newdescription, \
         "Got description = %s instead of %s" % (world.mynewprofile["description"], world.newdescription)
  
         
    #reset user to original state
    url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
    data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\""+world.myoldprofile["password"]+"\", \"description\":\""+world.myoldprofile["description"]+"\"}"
    world.mynewprofile = putJSONtoAPI(url, data)
@step('I enter a new invalid password "([^"]*)"')
def when_i_enter_a_new_invalid_password_group1(step, group1):
    world.password = group1
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/profile/"+str(world.user_id))
    if 'error' in result:
        world.error = result
        return error
    else:
        world.myoldprofile = result
        url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
        data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\""+group1+"\", \"description\":\""+world.myoldprofile["description"]+"\"}"
        world.mynewprofile = putJSONtoAPI(url, data)
     
@step('I should receive an error message')
def then_i_should_receive_an_error_message(step):
    assert world.error["error"] in ['length should be at least 6', 'Password should have at least one numeral', 'Password should have at least one uppercase letter', 'Password should have at least one lowercase letter', 'Password should have at least one of the symbols $@#'], \
        "Got error = %s"  % (world.error["error"])
    
# ID_010 View selected user profile

@step('I am logged in the application as an user with id = "([^"]*)"')
def given_i_am_logged_in_the_application(step, user_id):
    world.user_id = user_id
    

@step('When I view a user\'s profile with id (\d+)')
def view_user_profile(step, viewed_user_id):
    world.viewed_user_id = viewed_user_id
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/" + world.viewed_user_id)
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
    return response
    
def putJSONtoAPI(url, jsonvar):
    payload = jsonvar
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data = payload)
    return json.loads(response.text.encode('utf8'))
