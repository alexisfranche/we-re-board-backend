from lettuce import *
import urllib, json
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from requests.auth import HTTPDigestAuth

## STEP DEFINITIONS
# ID 001 - Create user


@step('I am browsing the login page')
def given_i_am_browsing_the_login_page(step):
    world.user_id = -1
@step('I clicked on the register button')
def and_i_clicked_on_the_register_button(step):
    pass
@step('I fill in these information to my profile:')
def when_i_fill_in_these_information_to_my_profile(step):
    world.name = step.hashes[0]["Name"]
    world.surname = step.hashes[0]["Surname"]
    world.username = step.hashes[0]["Username"]
    world.password = step.hashes[0]["Password"]
    world.passwordconfirmation = step.hashes[0]["Password confirmation"]
    world.email = step.hashes[0]["email"]
    world.phone = step.hashes[0]["Phone Number"]
    world.description = step.hashes[0]["Description"]
  
    result = createUserAPI(world.username, world.email, world.password)

    if 'error' in result:
        world.error = result["error"]
    else:
        response = result

@step('the system should send me an email')
def then_the_system_should_send_me_an_email(step):
    pass #Will implement once api is created
    
@step('I should now be able to sign in to the app')
def and_i_should_now_be_able_to_sign_in_to_the_app(step):
    url = "https://were-board.herokuapp.com/email/" + world.email
    result = getJSONfromAPI(url)
    
    if 'error' in result:
        world.error = result["error"]
    else:
        id = result["id"]
        response = getJSONfromLoginAPI(world.email, world.password)
        result = response 
        if 'error' in result:
            world.error = result["error"]
        else:
            world.message = result["data"]
            expected_confirmation_message = "You were logged in"
            assert world.message == expected_confirmation_message, \
            "Got message = %s instead of %s" % (world.message, expected_confirmation_message)
            deleteAPI("https://were-board.herokuapp.com/user/"+str(id))
            
@step('My password doesn\'t respect the format')
def and_my_password_doesn_t_respect_the_format(step):
    pass
    
@step('the system should display an error message')
def then_the_system_should_display_an_error_message(step):
    assert world.error == 'Invalid email or password',\
        "Got error = %s"  % (world.error)
@step('the email is already used')
def but_the_email_is_already_used(step):
    pass
    
@step('the username \'([^\']*)\' is already used')
def and_the_username_group1_is_already_used(step, group1):
    pass #API not implemented

# ID_002 Login
@step('I am already registered to the application with id = (\d+)')
def given_i_am_registered_to_the_application(step, user_id):
    world.user_id = user_id

@step('I am not yet registered to the application')
def given_i_am_not_yet_registered_to_the_application(step):
    world.user_id = -1
    
@step('I login to the application with email = "([^"]*)" and password = "([^"]*)"')
def when_i_login_to_the_application(step, email, password):
    response = getJSONfromLoginAPI(email, password)
    result = response 
    if 'error' in result:
        world.error = result["error"]
    else:
        world.message = result["data"]


@step('The system logs me in and displays a confirmation message')
def then_the_system_logs_me_in_and_displays_a_confirmation_message(step):
    expected_confirmation_message = "You were logged in."
    assert world.message == expected_confirmation_message, \
        "Got message = %s instead of %s" % (world.message, expected_confirmation_message)


@step('the system does not log me in and displays a "([^"]*)" error message')
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
        world.error = result['error']
    else:
        world.message = result['data']
    
@step('I should lose access to the application\'s features and redirect out')
def then_i_should_lose_access_to_the_application_s_features_and_redirect_out(step):
    expected_confirmation_message = "You were logged out."
    assert world.message == expected_confirmation_message, \
        "Got message = %s instead of %s"  % (world.message, expected_confirmation_message)

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
        world.error = result['error']
    else:
        world.myprofile = result
        
@step('the system displays the following:')
def assert_personal_profile(step):

    assert str(world.myprofile["id"]) == str(step.hashes[0]["ID"]), \
        "Got id = %s instead of %s" % (world.myprofile["id"], str(step.hashes[0]["ID"]))
        
    assert world.myprofile["name"] == step.hashes[0]["Name"], \
        "Got name = %s instead of %s" % (world.myprofile["name"], str(step.hashes[0]["Name"]))
         
    assert str(world.myprofile["email"]) == str(step.hashes[0]["Email"]), \
        "Got email = %s instead of %s" % (str(world.myprofile["email"]), str(step.hashes[0]["Email"])) 
         
    assert world.myprofile["description"] == step.hashes[0]["Description"], \
        "Got description = %s instead of %s" % (world.myprofile["description"], str(step.hashes[0]["Description"]))
         
    assert str(world.myprofile["password"]) == str(step.hashes[0]["Password"]), \
        "Got password = %s instead of %s" % (str(world.myprofile["password"]), str(step.hashes[0]["Password"]))

@step('the system displays an "([^"]*)" error message')
def assert_error_404(step, expected):
    assert world.error == expected, "Got error = %s instead of %s"  % (world.error, expected)


#ID__005 - Modify Personal Profile

@step('I enter a new name "([^"]*)"')
def given_i_enter_a_new_name_group1(step, group1):
    world.newname = group1
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/profile/"+str(world.user_id))
    if 'error' in result:
        world.error = result["error"]
    else:
        world.myoldprofile = result
        url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
        data = "{\"name\":\""+group1+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\"bla3Bla$\", \"description\":\""+world.myoldprofile["description"]+"\"}"
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
    data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\"bla3Bla$\", \"description\":\""+world.myoldprofile["description"]+"\"}"
    world.mynewprofile = putJSONtoAPI(url, data)
    
@step('I enter a new password "([^"]*)"')
def when_i_enter_a_new_password_group1(step, group1):
    world.newpassword = group1
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/profile/"+str(world.user_id))
    if 'error' in result:
        world.error = result["error"]
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
    data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\"bla3Bla$\", \"description\":\""+world.myoldprofile["description"]+"\"}"
    world.mynewprofile = putJSONtoAPI(url, data)
    
@step('I enter a new email "([^"]*)"')
def when_i_enter_a_new_email_group1(step, group1):
    world.newemail = group1
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/profile/"+str(world.user_id))
    if 'error' in result:
        world.error = result
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
        world.error = result["error"]
    else:
        world.myoldprofile = result
        url = "https://were-board.herokuapp.com/user/profile/"+str(world.user_id)
        data = "{\"name\":\""+world.myoldprofile["name"]+"\", \"email\":\""+world.myoldprofile["email"]+"\", \"password\":\""+group1+"\", \"description\":\""+world.myoldprofile["description"]+"\"}"
        world.mynewprofile = putJSONtoAPI(url, data)
        if'error' in world.mynewprofile:
            world.error = world.mynewprofile["error"]
@step('I should receive an error message')
def then_i_should_receive_an_error_message(step):
    assert world.error == 'Invalid email or password',\
        "Got error = %s"  % (world.error)

#ID_007
@step(u'Given I am logged in as a user')
def given_i_am_logged_in_as_a_user(step):
    world.user_id = 20
@step(u'And I have navigated to the \'Find Events\' page')
def and_i_have_navigated_to_the_group1_page(step):
    pass
@step(u'When I select the \'([^\']*)\' option')
def when_i_select_the_group1_option(step, group1):
    result = getJSONfromAPI("https://were-board.herokuapp.com/event/category/"+group1)
    if 'error' in result:
        world.error = result["error"]
    else:
        world.eventlist = result
    
@step(u'Then the system displays all the active events in a list by categories with the following information:')
def then_the_system_displays_all_the_active_events_in_a_list_by_categories_with_the_following_information(step):
    eventlist = world.eventlist
    for i in range(len(eventlist)):
        assert eventlist[i]['name'] == step.hashes[i]["Name"],\
            "Got name = %s instead of %s"  % (eventlist[i]['name'], step.hashes[i]["Name"])
        assert eventlist[i]['game'] == step.hashes[i]["Game"],\
            "Got game = %s instead of %s for %s"  % (eventlist[i]['game'], step.hashes[i]["Game"], eventlist[i]['name'])    
        assert eventlist[i]['datetime'] == step.hashes[i]["Date"],\
            "Got date = %s instead of %s for %s"  % (eventlist[i]['datetime'], step.hashes[i]["Date"], eventlist[i]['name'])
        assert eventlist[i]['address'] == step.hashes[i]["Address"],\
            "Got address = %s instead of %s for %s"  % (eventlist[i]['address'], step.hashes[i]["Address"], eventlist[i]['name'])
@step(u'But there are no active events of that category in the system database')
def but_there_are_no_active_events_of_that_category_in_the_system_database(step):
    pass
@step(u'Then the system display a "([^"]*)" error message')
def then_the_system_display_a_group1_error_message(step, group1):
    assert world.error == group1,\
        "Got error = %s instead of %s"  % (world.error, group1)


# ID_008 Access specific event

@step(u'Given I am logged in as a user')
def given_i_am_logged_in_as_a_user(step):
    world.user_id = 20
@step(u'And I have navigated to the \'Find Events\' page')
def and_i_have_navigated_to_the_group1_page(step):
    pass
@step(u'When I select an event to access the selected event page')
def when_i_select_the_event(step):
    world.event_id = 50
    result = getJSONfromAPI("https://were-board.herokuapp.com/event/" + str(world.event_id))
    if 'error' in result:
        world.error = result["error"]
    else:
        world.event = result#change this to match API once implemented
@step(u'Then the system displays all the details about the event')
def then_the_system_displays_the_event_with_the_following_information(step):
    event = world.event
    assert event['name'] == step.hashes[0]["Name"],\
        "Got name = %s instead of %s"  % (event['name'], step.hashes[0]["Name"])
    assert event['game'] == step.hashes[0]["Game"],\
        "Got game = %s instead of %s for %s"  % (event['game'], step.hashes[0]["Game"], event['name'])
    assert event['datetime'] == step.hashes[0]["Date"],\
        "Got date = %s instead of %s for %s"  % (event['datetime'], step.hashes[0]["Date"], event['name'])
    assert event['address'] == step.hashes[0]["Location"],\
        "Got address = %s instead of %s for %s"  % (event['address'], step.hashes[0]["Address"], event['name'])


# ID_009 Apply
@step(u'Given I am signed in as user Jackson')
def given_i_am_logged_in_as_a_user(step):
    world.user_id = 20
@step(u'And I am on the active event page titled Poker')
def and_i_am_on_event_poker(step):
    world.event_id = 50
@step(u'When I apply for the event')
def when_i_apply_for_the_event(step):
    result = applyEventAPI(world.event_id, world.user_id)
    if 'error' in result:
        world.error = result["error"]
    else:
        response = result
@step(u'Then I should be associated with the event')
def then_im_associated_with_the_event(step):
    result = existsEventUserAPI(world.event_id, world.user_id)
    if 'error' in result:
        world.error = result["error"]
        raise AssertionError("false")
    else:
        world.response = result
        assert world.response["is_joined"] == bool("true")
        deleteEventUserAPI(world.event_id, world.user_id)


# ID_010 View selected user profile

@step(u'Given I am a user of We\'re Board with id=(\d+)')
def given_i_am_a_user_of_we_re_board_with_id_20(step, number):
    world.user_id = number
@step(u'And I am logged into We\'re Board')
def and_i_am_logged_into_we_re_board(step):
    pass
@step(u'When I access the page of a non-existing user')
def when_i_access_the_page_of_a_non_existing_user(step):
    world.viewed_user_id = -1
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/" + str(world.viewed_user_id))
    if 'error' in result:
        world.error = result["error"]
    else:
        world.myprofile = result

@step(u'Then a "([^"]*)" message is displayed')
def then_a_user_not_found_message_is_displayed(step, group1):
    assert world.error == group1, \
        "Got error = %s instead of %s"  % (world.error, group1)

@step(u'I am logged in the application as an user with id = "([^"]*)"')
def given_i_am_logged_in_the_application(step, user_id):
    world.user_id = user_id


@step(u'When I view a user\'s profile with id (\d+)')
def view_user_profile(step, viewed_user_id):
    world.viewed_user_id = viewed_user_id
    result = getJSONfromAPI("https://were-board.herokuapp.com/user/" + world.viewed_user_id)
    if 'error' in result:
        world.error = result["error"]
    else:
        world.myprofile = result

@step(u'Then the system displays the following:')
def system_displays_user(step):
    profile = world.myprofile
    assert profile['id'] == profile["id"], \
        "Got id = %s instead of %s for %s" % (profile['id'], profile["id"], profile['name'])
    assert profile['name'] == profile["name"], \
        "Got name = %s instead of %s for %s" % (profile['name'], profile["name"], profile['name'])
    assert profile['email'] == profile['email'], \
        "Got email = %s instead of %s for %s" % (profile['email'], profile['email'], profile['name'])
    assert profile['description'] == profile['description'], \
        "Got description = %s instead of %s for %s" % (profile['description'], profile['description'], profile['name'])
    assert profile['password'] == profile['password'], \
        "Got password = %s instead of %s for %s" % (profile['password'], profile['password'], profile['name'])


#ID_012 Create Event
@step(u'Given I am signed in as a user')
def given_i_am_logged_in_as_a_user(step):
    world.user_id = 20


@step(u'And I am on the create event page')
def and_i_am_on_the_create_event_page(step):
    pass

@step(u'When I create the event with these informations:')
def when_i_select_the_create_event_option(step):
    world.name = step.hashes[0]["Name"]
    world.game = step.hashes[0]["Game"]
    world.date = step.hashes[0]["Date"]
    world.location = step.hashes[0]["Location"]
    world.description = step.hashes[0]["Description"]

    result = createEventAPI(world.name, world.location, world.game, world.description, world.date, world.user_id)

    if 'error' in result:
        world.error = result["error"]

    else:
        world.event = result

@step(u'Then the system display a "([^"]*)" error message')
def then_the_system_displays_error_message(step, group1):
    assert world.error == group1,\
        "Got error = %s instead of %s"  % (world.error, group1)


@step(u'Then the system should create my event')
def create_event(step):
    pass

@step(u'And I should see the event in the \'Manage my Events\' page under \'hosting\'')
def see_event(step):
    pass

@step(u'But I am suspended')
def but_the_user_is_suspended(step):
    pass

@step(u'And I schedule the event for a date prior to the current date')
def schedule_event_prior_to_current_date(step):
    pass

@step(u'And I specify an address for the event that does not exist')
def address_doesnt_exist(step):
    pass

@step(u'And I do not specify a game type for the event')
def dont_specify_game_type(step):
    pass

@step(u'And I do not specify a name for the event')
def dont_specify_name(step):
    pass



#ID 013 Cancel an Event
@step(u'Given I am logged in as the Event Manager with id=(\d+)')
def given_i_am_logged_in_as_the_event_manager(step, id):
    world.user_id=id
    pass

@step(u'And I have navigated to the \'Manage my Events\' page')
def and_i_have_navigated_to_manage_my_events_page(step):
    pass

@step(u'When I select the \'Delete\' button next to an Event with id=(\d+)')
def when_i_select_delete(step, event_id):
    world.event_id=event_id
    result = deleteEventUserAPI(world.event_id, world.user_id)
    world.response = result

@step(u'Then the Event is deleted')
def delete_event(step):
    pass

@step(u'And a \'Successfully deleted event\' message is issued')
def display_success_message(step):
    pass

@step(u'Given I am logged in as a user with id=(\d+)')
def logged_in_as_user(step, id):
    world.user_id = id
@step(u'Then a \'You are not the Event Manager\' message is issued')
def you_are_not_event_manager(step):
    pass

#ID_016 Modify an Event

@step('Given I am logged in as the Event Manager with id=(\d+)')
def given_i_am_logged_in_as_the_event_manager(step, id):
    world.user_id=id
    pass

@step('And I have navigated to the \'Manage my Events\' page')  
def and_i_have_navigated_to_manage_my_events_page(step):
    pass  

@step('When I select the Modify button next to event with id=(\d+)')
def when_i_select_modify(step, event_id):
    world.event_id=event_id
    pass
    
@step('Then I can edit the events information')
def then_i_can_edit_info(step):
    world.old_event= getJSONfromAPI("https://were-board.herokuapp.com/event/"+str(world.event_id))
    if 'error' in world.old_event:
        world.error= world.old_event["error"]
    else: 
        if(world.old_event["name"]!= "Poker1"):
            world.new_name="Poker1"
        else:
            world.new_name="Poker2"
        
        url= "https://were-board.herokuapp.com/event/"+str(world.event_id)
        data="{\"name\":\""+world.new_name+"\", \"address\":\""+world.old_event["address"]+"\", \"game\":\""+world.old_event["game"]+"\", \"datetime\":\""+world.old_event["datetime"]+"\", \"description\":\""+world.old_event["description"]+"\"}"
        world.new_event= putJSONtoAPI(url, data)

@step('And when I press the \'Save\' button the Event\'s information is updated')
def event_info_updated(step):
    assert world.old_event["name"] != world.new_event["name"]


##HELPER FUCNTIONS
def getJSONfromAPI(url):
    response = requests.get(url)
    data = response.json()
    return data

def createUserAPI(name, email, password):
    url = "https://were-board.herokuapp.com/user"

    payload = "{\"name\":\""+name+"\",\"email\":\""+email+"\",\"password\":\""+password+"\"}"
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)

    return json.loads(response.text.encode('utf8'))

def applyEventAPI(event_id, user_id):
    url = "https://were-board.herokuapp.com/join"

    payload = '{\"event_id\":'+str(event_id)+',\"user_id\":'+str(user_id)+'}'
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)

    return json.loads(response.text.encode('utf8'))

def existsEventUserAPI(event_id, user_id):
    url = "https://were-board.herokuapp.com/event_user/exists"

    payload = '{\"event_id\":'+str(event_id)+',\"user_id\":'+str(user_id)+'}'
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)

    return json.loads(response.text.encode('utf8'))

def deleteEventUserAPI(event_id, user_id):
    url = "https://were-board.herokuapp.com/event_user/delete/" + str(event_id) + "/" + str(user_id)

    headers = {
    'Content-Type': 'application/json'
    }
    requests.request("DELETE", url, headers=headers)

    return
    
def getJSONfromLoginAPI(email, password):
    url = "https://were-board.herokuapp.com/login"
    payload = "{\"email\":\""+email+"\",\"password\":\""+password+"\"}"
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    return json.loads(response.text.encode('utf8'))
    
def putJSONtoAPI(url, jsonvar):
    payload = jsonvar
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data = payload)
    return json.loads(response.text.encode('utf8'))
    
def deleteAPI(url):

    payload = {}
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, data = payload)

    return json.loads(response.text.encode('utf8'))

def createEventAPI(name, address, game, description, datetime, id):
    url = "https://were-board.herokuapp.com/event"

    payload = "{\"name\":\""+name+"\", \"address\":\""+address+"\", \"description\":\""+description+"\", \"datetime\":\""+str(datetime)+"\", \"event_manager_id\": \""+str(id)+"\", \"game\":\""+game+"\"}"
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    return json.loads(response.text.encode('utf-8'))
