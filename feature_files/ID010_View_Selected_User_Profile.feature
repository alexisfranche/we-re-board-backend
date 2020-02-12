Feature: View selected user profile

As a user of the "We're Board" app, I would like to be able to access another user's profile 
so I can decide whether or not to interact with this user

Background:
	Given I am a user of We're Board
	And I am logged into We're Board

Scenario: Viewing user succesfully (Normal flow)

When I click on a user's profile
Then The system displays the name of that user, a profile picture and a short description made by the user

Scenario: Viewing a non-existing user's profile (Error flow)

When I access the page of a non-existing user
Then A "This user does not exist" message is displayed


