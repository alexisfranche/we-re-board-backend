Feature: Apply for an Event

As a user of the "We're Board" app, I would like to rate an event in the app 
so that I can inform all the other users how satisfied I was with the event.

	Scenario: Rate an event as a normal user
	
		Given I am signed in as user Jackson
		And I am on the event page titled Poker by accessing it through ManageMyEvents
		When I rate the event 
		Then event should be rated
			

		
		
