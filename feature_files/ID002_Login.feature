Feature: Login to the app

As a registered user of the "We're Board" app, I would like to login to the app 
so that I can use the application.

	Scenario: Login to the app
	
	Normal Flow - The system should log me into the app
	
		Given the following user has already registered
        	|Name |Surname |Username|Password|Password confirmation|email            |Phone Number|Description|
			|Amine|Alikacem|Amine   |bla3Bla;|bla3Bla;             |amine@outlook.ca |15143334444 | blabla    |
		And I am on the login page
		When I enter "Amine" on the Username field
        And I enter "bla3Bla;" on the Password field
        And I press the "login" button
		Then I see the "home" page
			
	Scenario: Login to the app with a username that hasn't been registered
	
	Error Flow - The system display an error message
	
		Given the following user is the only one registered 
            |Name |Surname |Username|Password|Password confirmation|email            |Phone Number|Description|
			|Amine|Alikacem|Amine   |bla3Bla;|bla3Bla;             |amine@outlook.ca |15143334444 | blabla    |
		And I am browsing the login page
		When I enter "Amie" on the Username field
        And I enter "bla3Bla;" on the Password field
        And I press the "login" button
		Then the system should display an error message
        And stay on the login page

	Scenario: Login to the app with an incorrect password
	
	Error Flow - The system should display an error message
	
		Given the following user is the only one registered 
            |Name |Surname |Username|Password|Password confirmation|email            |Phone Number|Description|
			|Amine|Alikacem|Amine   |bla3Bla;|bla3Bla;             |amine@outlook.ca |15143334444 | blabla    |
		And I am browsing the login page
		When I enter "Amine" on the Username field
        And I enter "bla3" on the Password field
        And I press the "login" button
		Then the system should display an error message
        And stay on the login page


	

		
	