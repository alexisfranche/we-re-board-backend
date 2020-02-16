  
  Feature: Login to the app
  
  As a registered user of the "We're Board" app, I would like to login to the app 
  so that I can use the application.
  
  Scenario: Login to the app (Normal Flow)
  
    Given I am already registered to the application with id=26
     When I login to the application with email = "amine@outlook.ca" and password = "bla3Bla;"
     Then the system logs me in and displays a confirmation message
  
  Scenario: Login to the app with an email that hasn't been registered (Error Flow)
  
    Given I am not yet registered to the application
     When I login to the application with email = "notRegistered@outlook.ca" and password = "bla3Bla;"
     Then the system does not log me in and displays a "Not found" error message
  
  Scenario: Login to the app with an incorrect password (Error Flow)
  
    Given I am already registered to the application with id=26
     When I login to the application with email = "amine@outlook.ca" and password = "bla4Pla;"
     Then the system does not log me in and displays a "Invalid Credentials. Please try again." error message
  
  
