Feature: Apply for an Event

As a user of the "We're Board" app, I would like to apply for an event in the app 
so that I can inform the event manager of my interest.

	Scenario: Apply for an active event as a normal user - Normal Flow
		
		Given I am signed in as user Jackson
		And I am on the active event page titled Poker
		When I apply for the event 
		Then I should be associated with the event

		
		
