Feature: Modify personal profile information

As a user of the "We're Board" app, I would like to be able to 
modify my personal profile information so I can keep it accurate.

Scenario: Changing name successfully
	Given I am logged in the application as an user with id = "6"
	When I enter a new name "Josh"
	Then the system displays my new name on my profile page 

Scenario: Changing password successfully
	Given I am logged in the application as an user with id = "6" and email = "old@email.com"
	When I enter a new password "123Aa!"
	Then the system saves my new password

Scenario: Changing email to a new valid email
	Given I am logged in the application as an user with id = "6" and email = "old@email.com"
	When I enter a new email "newemail@email.com"
	Then The system saves my email
        
Scenario: Changing profile description
	Given I am logged in the application as an user with id = "6" and email = "old@email.com"
	When I change my profile description to "Great"
	Then The system saves my new profile description

Scenario: Changing password fails due to invalid password - Error Flow
	Given I am logged in the application as an user with id = "6" and email = "old@email.com"
	When I enter a new invalid password "badpassword"
	Then I should receive an error message
