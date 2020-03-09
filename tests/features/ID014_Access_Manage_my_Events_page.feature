Feature: Access 'Manage my Events' page

As a WereBoard User
I would like to access the 'Manage my Events' page
So that I can view all the events I am involved in

Scenario: View 'Manage my Events' page successfully (Normal Flow)

Given I am logged in as a user with id=2
And they manage an event with the id=51
When I select the 'Manage my Events' tab
Then the system displays some information about the events they manage


    
