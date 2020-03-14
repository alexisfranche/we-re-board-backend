Feature: Rate a Participant

As a user of the "We're Board" app, I would like to rate a participant in one of the events that I have attended 
so that I can inform all the other users how satisfied I am with this participant's behaviour.

	Scenario: Rate a valid participant in a valid attended event by myself (Normal Flow)
	
		Given I am signed in as user Jackson
		And I am on the event page titled Poker by accessing it through ManageMyEvents
		When I rate a valid participant who also attended this event 
		Then the rating should show up on this participant's profile

	Scenario: Rate a valid participant where we don't share common events (Error Flow)
			
		Given I am signed in as user Jackson
		And I am on the event page titled Poker by accessing it through ManageMyEvents
		When I rate a participant who didn't attended this event 
		Then I should not be able to rate this participant
		And get an error message saying: "User did not attend this event, you can't rate this user unless you select a common event"

	Scenario: Rate an InValid participant (Error Flow)
			
		Given I am signed in as user Jackson
		And I am on the event page titled Poker by accessing it through ManageMyEvents
		When I rate a participant who doesn't exist 
		Then I should get an error saying: "user does not exist"

	Scenario: Rate a user without selecting an event (Error Flow)
			
		Given I am signed in as user Jackson
		And I am not on an event page on ManageMyEvents
		When I attempt to rate a participant
		Then I should not be able to rate any participant
		And get the following error message: "You need to select an event first to be able to rate participants that attended it"
