class JsonData:
    POSITIVE_TEST_CASES_EXAMPLE = """
    Test Case 1: Navigate to Symptom Tracker Flow
Scenario:
A user selects the 'Identify patterns and triggers' tile on the home screen.
 
Pre-condition:
 
User is on the home screen of the app.
 
Steps:
 
Log in to the app.
 
Navigate to the home screen.
 
Tap on the 'Identify patterns and triggers' tile.
 
Expected Results:
 
The user is navigated into the Symptom Tracker flow with updated header designs.
 
Test Case 2: Log a Pain Location and Use the Visual Analogue Scale
Scenario:
A user logs a pain location and rates the pain using the visual analogue scale.
 
Pre-condition:
 
User is in the Symptom Tracker flow.
 
Steps:
 
Log a pain location on the body using the provided options.
 
Use the visual analogue scale to rate the pain (0 to 10).
 
Verify that the selected number is displayed at the top of the screen.
 
Expected Results:
 
The pain location is logged successfully.
 
The selected pain level is recorded and displayed at the top of the screen.
 
Test Case 3: Select 'What Made Your Pain Worse'
Scenario:
A user logs additional details about what made the pain worse.
 
Pre-condition:
 
User is in the Symptom Tracker flow and has logged a pain location and level.
 
Steps:
 
Navigate to the 'What made your pain worse' section.
 
Select multiple items from the list provided.
 
Verify that the selected items are recorded and displayed at the top of the screen.
 
Expected Results:
 
The selections are successfully recorded and displayed at the top of the screen.
 
Test Case 4: Successfully Log Symptoms
Scenario:
A user completes the Symptom Tracker flow.
 
Pre-condition:
 
User has logged all required symptom details.
 
Steps:
 
Enter the date and time for the symptoms.
 
Tap on the 'Done' CTA.
 
Verify that the new 'Symptoms logged' screen is displayed.
 
Expected Results:
 
The 'Symptoms logged' screen is displayed with the appropriate title and copy.
 
If no medication reminders are set:
 
The cross-promo for medication reminders is displayed.
 
Tapping 'Set reminder' navigates the user to the medication reminder screen.
 
If medication reminders are already set:
 
The illustration screen is displayed instead.
 
Tapping 'View calendar' navigates the user to the symptom history screen.
 
Test Case 5: View Symptom Tracking History
Scenario:
A user views the symptom history on the calendar screen.
 
Pre-condition:
 
User has logged at least one symptom.
 
Steps:
 
Navigate to the calendar screen.
 
Verify the following:
 
Title: "Calendar."
 
Sub-heading: "Symptom tracking history."
 
Copy: "Understanding your health: The importance of symptom tracking for effective medication management."
 
View the calendar.
 
Navigate to dates with and without logged symptoms.
 
Select a date with logged symptoms.
 
Expected Results:
 
Dates with logged symptoms have a green dot.
 
For selected dates with logged symptoms, the following is displayed:
 
Copy: "Successfully logged the following symptoms."
 
Time and symptom details as per the designs.
 
Test Case 6: Reinstalling the App
Scenario:
A patient reinstalls the app after uninstalling it.
 
Pre-condition:
 
Patient has logged symptoms in the app previously.
 
Steps:
 
Uninstall the app.
 
Reinstall and log in to the app.
 
Navigate to the Symptom Tracker.
 
Expected Results:
 
The patient is shown the intro screen for symptom tracking again.
    """

    NEGATIVE_TEST_CASES_EXAMPLE = """Negative Test Case 1: Modal Closed 3 Times via Close Button
	•	Scenario: User closes the modal via "X" icon three times.
	•	Precondition:
	◦	Feature flag enabled.
	◦	CE data exists.
	◦	User previously closed modal 3 times via close button.
	•	Steps:
	◦	User logs in again.
	•	Expected Result:
	◦	Modal does not reappear (respects the max 3 close logic).
	◦	App loads homescreen properly.

Negative Test Case 2: CTA Click but CPDB Save Fails
	•	Scenario: User clicks "Thanks for the reminder", but there's a backend failure.
	•	Precondition:
	◦	CE trigger exists.
	◦	Feature flag enabled.
	◦	Network is flaky or CPDB service is down.
	•	Steps:
	◦	Click on "Thanks for the reminder".
	•	Expected Result:
	◦	Modal closes.
	◦	Toaster message still appears.
	◦	App logs the failure to CPDB silently without affecting UX.

Negative Test Case 3: Incomplete User Profile Data
	•	Scenario: A user has an incomplete or corrupted referral record.
	•	Precondition:
	◦	Feature flag enabled.
	◦	CE record is malformed or has null fields.
	•	Steps:
	◦	User logs in.
	•	Expected Result:
	◦	Modal is not shown.
	◦	App does not crash and logs the error gracefully.

Negative Test Case 4: Modal Loads with Missing Image or Assets
	•	Scenario: Image asset for the modal is missing or fails to load.
	•	Precondition:
	◦	Feature flag enabled.
	◦	CE trigger exists.
	◦	Network fails to load image.
	•	Steps:
	◦	User logs in, modal triggers.
	•	Expected Result:
	◦	Modal still shows with text and CTA.
	◦	Image placeholder is handled gracefully (e.g., shows fallback or alt text).
	◦	No crash or broken UI.
    """

