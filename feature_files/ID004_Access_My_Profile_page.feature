Feature: View personal profile information

As a user of the "We're Board" app, I would like to be able to 
view my personal profile information so I modify it if necessary.

Scenario: View personal profile successfully (Normal Flow)
Given I am logged in as jackson@gmail.com
When I view my profile
Then the system displays the following:
	|	ID	|	Name  		|	Email			|	Description	|
	|	20	|	"Jackson"	|	"jackson@gmail.com"	|	"I like cake"	|
	
Scenario: View personal profile as a deleted user (Error Flow)
Given I am logged in as jackson@gmail.com
But my account is deleted
When I view my profile
Then the system displays an "User deleted" error message
	
Scenario: View personal profile when not connected to Wifi (Error Flow)
Given I am logged in as jackson@gmail.com
But I am not connected to Wifi
When I view my profile
Then the system displays an "Cannot connect to server" error message