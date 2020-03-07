Feature: View selected user profile

As a user of the "We're Board" app, I would like to be able to access another user's profile 
so I can decide whether or not to interact with this user


Scenario: Viewing user succesfully (Normal flow)

	Given I am a user of We're Board with id=20
	 And I am logged into We're Board
    When I view a user's profile with id 6
    Then the system displays the following:
	    |	ID	|	Name  		|		Email	|	Description		| Password |
	    |	6	|   Oldname		|		None	|	old Bio	        | 	None   |

Scenario: Viewing a non-existing user's profile (Error flow)

	Given I am a user of We're Board with id=20
	And I am logged into We're Board
	When I access the page of a non-existing user
	Then a "User Not found" message is displayed


