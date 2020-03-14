Feature: Back out of an Event

As a user of the "We're Board" app, I would like to back out of an event in the app 
so that I no longer have to attend it.

	Scenario: Back out of an event as a normal user
	
		Given I am signed in as user Jackson
		And I am on the event page titled Poker by accessing it through ManageMyEvents
		When I back out of the event 
		Then I should no longer be associated with it
			

		
		
