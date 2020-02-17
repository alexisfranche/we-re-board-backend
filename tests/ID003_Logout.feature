  Feature: Logout of the app
  
  As a registered user of the "We're Board" app, I would like to logout of the app 
  so that I exit the application.
  
  Scenario: Logout to the app successfully (Normal Flow)
    
    Given I am logged in the application as an user with id = 20
     When I log out of the application
     Then I should lose access to the application's features and redirect out
  
 
  
  
