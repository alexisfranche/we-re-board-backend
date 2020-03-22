Feature: Delete Account

As a user of the "We're Board" app, I would like to delete my existing account
so that my account information is no longer in the system's database.

	Scenario: Delete an existing account successfully (Normal Flow)
	
		Given I am signed in as user with id=INSERT_TEST_ID_HERE
		When click on the Delete Account button
		Then a message should appear saying "Account has successfully been deleted."
        And when i try to log back in with my deleted information, it should display a a "Invalid Credentials. Please try again." error message
