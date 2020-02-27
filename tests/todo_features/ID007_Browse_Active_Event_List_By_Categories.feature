Feature: Browse active event list by categories

As a user of the "We're Board" app, I would like to be able to browse active event list by categories so that I can find an event I'm interested in.

  Scenario: Browse active events list by categories successfully (Normal Flow)

    Given I am logged in as a user
      And I have navigated to the 'Find Events' page
     When I select the 'list by categories' option
     Then the system displays all the active events in a list by categories with the following information:
      | Name                        | Game  | Date       |
      | Friendly poker at my place! | Poker | 07/02/2020 |

  Scenario: Browse active events list by categories when no active events (Error Flow)

    Given I am logged in as a user
      And I have navigated to the 'Find Events' page
     When I select the 'list by categories' option
      But  there are no active events exist in the system database
     Then the system display a "No active event exist. Please try again later" error message
