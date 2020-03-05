Feature: Access selected event page

As a user of the "We're Board" app, I would like to be able to Access selected event page so that I can view more information about the event.

  Scenario: View 'Find Event' page successfully (Normal Flow)

    Given I am logged in as a user
      And I have navigated to the 'Find Events' page
     When I select an event to access the selected event page
     Then the system displays all the details about the event:
      | Name                        | Game  | Date       | Location                                         | Description |
      | Friendly poker at my place! | Poker | 07/02/2020T04:00:00+00:00 | 3448 Rue Clark, Montréal, Québec H2S 3G5, Canada | blabla      |
