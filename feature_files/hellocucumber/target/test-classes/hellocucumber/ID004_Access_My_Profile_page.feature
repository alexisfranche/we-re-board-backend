Feature: View personal profile information

As a user of the "We're Board" app, I would like to be able to 
view my personal profile information so I modify it if necessary.

Scenario: View personal profile successfully (Normal Flow)
Given I am logged in as an user with id=20
When I view my profile
Then the system displays the following:
	|	ID	|	Name  	|		Email			|	Description	| Password |
	|	20	|	jackson	|	jackson@gmail.com	|	I like cake	| pbkdf2:sha256:150000$Yulbep3A$5200882852aed7add39d11cdcb0b7fb082345653605ef0a1295a63856b3dee5c |
	
Scenario: View personal profile as a deleted user (Error Flow)
Given I am logged in as an user with id=20
But my account is deleted
When I view my profile
Then the system displays an "Not found" error message
