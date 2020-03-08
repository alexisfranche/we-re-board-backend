  Feature: Access 'Find Event' page
  
  As a user of the "We're Board" app, I would like to be able to access the 'Find Event' page with a list of all the active events so that I can I can find an event to participate in.
  
  Scenario: View 'Find Event' page successfully (Normal Flow)
  
    Given I am logged in as a user
     When I have navigated to the 'Find Events' page
     Then the system displays the list of all active events in which I can participate
  
  Scenario: View 'Find Event' page when no active events exist (Error Flow)
  
    Given I am logged in as a user
      And no active events exist in the system database
     When I have navigated to the 'Find Events' page 
     Then I should receive an error message
  
