Feature: View selected user profile

As a user of the "We're Board" app, I would like to be able to access another user's profile 
so I can decide whether or not to interact with this user

Background:
	Given I am a user of We're Board with id=20
	And I am logged into We're Board

Scenario: Viewing user succesfully (Normal flow)

|	ID	|	Name  	|		Email			|	Description	| Password |
|	6	|   randomuser	|	random555@gmail.com	        |	Hello	        | pbkdf2:sha256:150000$6Wl2CGr8$e38868d346e21f9094a7b4cd63849d7fb12a52c5d8674ffeff8697fba789dc85 |

When I view a user's profile with id 6
Then The system displays the name <Name>, a default profile picture and a short description <Description> made by the user

Scenario: Viewing a non-existing user's profile (Error flow)

When I access the page of a non-existing user
Then A "This user does not exist" message is displayed


