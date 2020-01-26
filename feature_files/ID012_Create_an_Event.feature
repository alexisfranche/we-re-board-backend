Feature: Create an Event

As a user of the "We're Board" app, I would like to create an event in the app 
so that I can let other users know about my event.

	Scenario: Create an event as a normal user

	Normal Flow - The system should create the event for other users to see
	
		Given I am signed in as user Pierre
		And I am on the create event page
		When I create the event 
		Then the system should create my event
		And I should see the event in the 'Manage my Events' page under 'hosting'
			
	Scenario: Create an event as a suspended user
	
	Alternate Flow - The system should not create the event
	
		Given I am signed in as user Pierre
		And I am on the create event page
		But I am suspended
		When I create the event 
		Then I should receive a suspension reminder message

	Scenario: Create an event for an invalid date as a normal user
	
	Error Flow - The system should not create the event
	
		Given I am signed in as user Pierre
		And I am on the create event page
		But I schedule the event for a date prior to the current date
		When I create the event 
		Then I should receive an error message

	Scenario: Create an event for an invalid address as a normal user
	
	Error Flow - The system should not create the event
	
		Given I am signed in as user Pierre
		And I am on the create event page
		But I specify an address for the event that does not exist
		When I create the event 
		Then I should receive an error message
		
