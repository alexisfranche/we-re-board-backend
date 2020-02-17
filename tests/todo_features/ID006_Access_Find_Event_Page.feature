Feature: Access 'Find Event' page

As a user of the "We're Board" app, I would like to be able to access the 'Find Event' page so that I can I can find an event to participate in.

  Scenario: View 'Find Event' page successfully (Normal Flow)

    Given I am logged in as a user
     When I try to access the Find Event page
     Then the system displays the Find Event page
      And allows me to find events to participate in

  Scenario: View 'Find Event' page when no active events exist (Error Flow)

    Given I am logged in as a user
     When I try to access the Find Event page
      But no active events exist in the system database
     Then the system display a "No active event exist. Please try again later" error message
