  Feature: Logout of the app
  
  As a registered user of the "We're Board" app, I would like to logout of the app 
  so that I exit the application.
  
  Scenario: Logout to the app successfully
  
  Normal Flow - The system should log me out from the app
  
    Given I am logged in the application
     When I log out of the application
     Then I should lose access to the application's features and redirect out
  
 
  
  
