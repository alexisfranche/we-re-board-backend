
Feature: Modify an Event

As a WereBoard Event Manager
I would like to modify an event
So that I can update the event's information

Scenario Outline: Event Manager modifies an Event (Normal Flow)

Given I am logged in as the Event Manager with id=1
And I have navigated to the 'Manage my Events' page
When I select the Modify button next to Event with id=31
Then I can edit the events information
And when I press the 'Save' button the Event's information is updated


