Feature: Browse active event list by categories

As a user of the "We're Board" app, I would like to be able to browse active event list by categories so that I can find an event I'm interested in.

  Scenario: Browse active events list by categories successfully (Normal Flow)

    Given I am logged in as a user
      And I have navigated to the 'Find Events' page
     When I select the 'monopoly' option
     Then the system displays all the active events in a list by categories with the following information:
		| Name             		        | Game  	| Date      		 		|	Address				|
		| Monopoly Time					| monopoly 	| 2020-04-08T04:05:06+00:00	|	200 Collect Street	|
		| Monopoly 2: Electric Boogaloo	| monopoly 	| 2020-05-08T04:05:06+00:00 |	200 Collect Street	|
	  

  Scenario: Browse active events list by categories when no active events of that category (Error Flow)

    Given I am logged in as a user
      And I have navigated to the 'Find Events' page
     When I select the 'knucklebones' option
     But there are no active events of that category in the system database
     Then the system display a "No active events of this category." error message
