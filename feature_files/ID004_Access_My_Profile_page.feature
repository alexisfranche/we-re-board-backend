Feature: View my profile

As a user of the "We're Board" app, I would like to be able to access my user profile 
so I can witness the information linked to my profile

Background:
	Given I am a user of We're Board with id=6
	And I am logged into We're Board

Scenario: Viewing my profile successfully (Normal flow)

|	ID	|	Name  	|		Email			|	Description	| Password |
|	6	|  randomuser	|	random555@gmail.com   |	Hello	    | pbkdf2:sha256:150000$6Wl2CGr8$e38868d346e21f9094a7b4cd63849d7fb12a52c5d8674ffeff8697fba789dc85 |

When I view my profile with id 6
Then The system displays the name <Name>, a default profile picture and a short description <Description> made by the user


