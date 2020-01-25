Feature: Modify personal profile information

As a user of the "We're Board" app, I would like to be able to 
modify my personal profile information so I can keep it accurate.

Background:
	Given I am a user of We're Board
	And I am logged into We're Board

Scenario: Changing name successfully
Given I enter a new name 
Then The system saves my new name
And The system displays my new name on my profile page 

Scenario: Changing password successfully
Given I enter a new password 
Then The system saves my new password

Scenario: Changing email to a new valid email
Given I enter a new email 
Then The system saves my email

Scenario: Changing email fails due to invalid email

Error Flow - The system should not save the new email

Given I enter a new invalid email 
Then I should receive an error message
        
Scenario: Changing profile picture successfully

Given I choose a profile picture 
Then The system saves my new profile picture

Scenario: Changing profile description
Given I change my profile description
Then The system saves my new profile description

