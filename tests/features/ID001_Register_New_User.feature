  Feature: Register a user
  
  As an upcoming user of the "We're Board" app, I would like to register to the app 
  so that I can use the application.
  
  Scenario: Register to the app
    
    Given there is no user registered with the email 'test1@email.com'
    When I submit the following information to the sign-up form:
      |  name  |      email      |   password     | 
      |  Test  | test1@email.com | testPassword1% |
    Then I should be able to sign in to the app with the provided email and password

  
  Scenario: Register to the app with a password that is 2 characters or less
    
    Given there is no user registered with the email 'test1@email.com'
    When I submit the following information to the sign-up form:
      |  name  |      email      |   password   |
      |  Test  | test1@email.com |     yo       |
    Then the system should send an error message
 
  Scenario: Register to the app with an email that is not valid
  
    When I submit the following information to the sign-up form:
      |  name  |           email         |   password   |
      |  Test  |         notAnEmail      | testPassword1% |
    Then the system should send an error message
  
  
