Feature: Cancel an Event

As a WereBoard Event Manager
I would like to cancel an event
So that I can let other participants know and prevent more applications to join the event

Scenario Outline: Event Managaer requests to cancel an Event (Normal Flow)

Given I am logged in as the Event Manager
And I have navigated to the "My Events" page
When I select the "Delete" button next to an Event
Then a "Successfully deleted event" message is issued

Scenario Outline: Event Manager requests to cancel an Event that has already occured (Error Flow)

Given I am logged in as the Event Manager
And I have navigated to the "My Events" page
When I select the "Delete" button next to an Event
Then a "Event has already occired" message is issued
