  Feature: Register a user
  
  As an upcoming user of the "We're Board" app, I would like to register to the app 
  so that I can use the application.
  
  Scenario: Register to the app - Normal Flow

  
    Given I am browsing the login page
      And I clicked on the register button
     When I fill in these information to my profile:
      | Name  | Surname  | Username | Password | Password confirmation | email            | Phone Number | Description | 
      | Amine | Alikacem | Amine    | bla3Bla; | bla3Bla;              | amine@outlook.ca | 15143334444  | blabla      | 
     Then the system should send me an email
      And I should now be able to sign in to the app
  
  Scenario: Register to the app with a password that doesn't respect the format - Error flow
 
  
    Given I am browsing the login page
      And I clicked on the register button
     When I fill in these information to my profile:
      | Name  | Surname  | Username | Password | Password confirmation | email            | Phone Number | Description | 
      | Amine | Alikacem | Amine    | bla      | bla                   | amine@outlook.ca | 15143334444  | blabla      | 
      And My password doesn't respect the format
     Then the system should display an error message
  
  Scenario: Register to the app with a password and a password confirmation that don't match - Error flow
  
  
    Given I am browsing the login page
      And I clicked on the register button
     When I fill in these information to my profile:
      | Name  | Surname  | Username | Password | Password confirmation | email            | Phone Number | Description | 
      | Amine | Alikacem | Amine    | bla3Bla; | bla444Bla;            | amine@outlook.ca | 15143334444  | blabla      | 
     Then the system should display an error message
  

  Scenario: Register to the app with a username that already exists - Error flow
  
    Given I am browsing the login page
      And I clicked on the register button
     When I fill in these information to my profile:
      | Name  | Surname  | Username | Password | Password confirmation | email            | Phone Number | Description | 
      | Amine | Alikacem | Jack    | bla3Bla; | bla3Bla;              | amine@outlook.ca | 15143334444  | blabla      | 
      And the username 'Jack' is already used
     Then the system should display an error message
  

  Scenario: Register to the app with an email that is not valid
  
  
    Given I am browsing the login page
      And I clicked on the register button
	  But the email is already used
     When I fill in these information to my profile:
      | Name  | Surname  | Username | Password | Password confirmation | email 	 | Phone Number | Description | 
      | Amine | Alikacem | Amine    | bla3Bla; | bla3Bla;              | email	 | 15143334444  | blabla      | 
     Then the system should display an error message
  
  
