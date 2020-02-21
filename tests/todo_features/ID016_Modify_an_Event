Feature: Modify an Event

As a WereBoard Event Manager
I would like to modify an event
So that I can update the event's information

Scenario Outline: Event Manager modifies an Event (Normal Flow)

Given I am logged in as the Event Manager
And I have navigated to the 'Manage my Events' page
When I select the 'Modify' button next to Event Poker
Then I can edit the events information
And when I press the 'Save' button the Event's information is updated


Scenario Outline: Unauthorized User requests to cancel an Event (Error Flow)

Given I am logged in as a user
And I have navigated to the "Manage my Events" page
When I select the 'Delete' button next to an Event
Then a "You are not the Event Manager" message is issued
