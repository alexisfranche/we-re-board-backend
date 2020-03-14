
Feature: Kick out an event participant

As a WereBoard Event Manager
I would like to kick out an event participant from my event
So that the user is no longer an event participant

Scenario: Event Manager kicks a user out of event (Normal Flow)

Given I am logged in as the user with id=1
And I am the event manager for event with id=31
When kick out user with id=20 from the event
Then that user should no longer be associated to the event