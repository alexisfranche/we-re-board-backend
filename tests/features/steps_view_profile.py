from lettuce import *
import urllib, json


## STEP DEFINITIONS

# ID_010 View selected user profile

@step('I am logged in the application as an user with id = (\d+)')
def given_i_am_logged_in_the_application(step, user_id, email):
    world.user_id = user_id
    world.email = email

@step('my account does not exist')
def have_non_valid_user_id(step):
    world.user_id = -1
    world.email = -1


@step('I view user with given id')
def view_user_profile(step):
    result = getJSONfromAPI("https://were-board.herokuapp.com//user/profile/" + str(world.user_id))
    if 'error' in result:
        world.error = result
    else:
        world.profile = result


@step('the system displays the following:')
def assert_user_profile(step):
    assert str(world.profile["id"]) == str(step.hashes[0]["ID"]), \
        "Got id = %s instead of %s" % (world.profile["id"], str(step.hashes[0]["ID"]))

    assert world.profile["name"] == step.hashes[0]["Name"], \
        "Got name = %s instead of %s" % (world.profile["name"], str(step.hashes[0]["Name"]))

    assert world.profile["description"] == step.hashes[0]["Description"], \
        "Got description = %s instead of %s" % (world.profile["description"], str(step.hashes[0]["Description"]))


@step('the system displays an "([^"]*)" error message')
def assert_error_404(step, expected):
    assert world.error["error"] == expected, \
        "Got error = %s instead of %s" % (world.error["error"], expected)


##HELPER FUCNTIONS
def getJSONfromAPI(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data