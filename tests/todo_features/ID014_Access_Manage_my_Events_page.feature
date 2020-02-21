Feature: Access 'Manage my Events' page

As a WereBoard User
I would like to access the 'Manage my Events' page
So that I can view all the events I am involved in

Scenario: View 'Manage my Events' page successfully (Normal Flow)

Given I am logged in as a user
When I select the 'Manage my Events' tab
Then the system displays some information about the event:

      | Name                        | Game    | Date       |
      | Friendly poker at my place! | Poker   | 07/02/2020 |
      | Competitive Monopoly        | Monopoly| 07/10/2020 |

 Scenario: View 'Manage my Events' when there are no events (Alternate Flow)

Given I am logged in as a user
When I select the 'Manage my Events' tab
Then a "No active event exist. Please try again later" message is issued

    
