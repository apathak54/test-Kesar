from test_case_agent import process_input
import os
from dotenv import load_dotenv
from config import JsonData

# Load environment variables
load_dotenv()

def main():
    # Example PBI from input_output.txt
    pbi = """
    AC-1 Symptom Tracking
    Given I am on the home screen
    When I action the 'Identify patterns and triggers' tile
    Then I am navigated into the Symptom tracker flow
    Please adhere to the new designs (change in headers design)
    After logging a location for the pain there is now a visual analogue scale
    The scale is from 0 to 10
    0 = Not painful
    10 = Extremely painful
    Record the selection (number selected) at the top of the screen as shown in the designs
    """
  
    # Process the input
    result = process_input(pbi, JsonData.POSITIVE_TEST_CASES_EXAMPLE, JsonData.NEGATIVE_TEST_CASES_EXAMPLE)
    
    # Print results
    print("Positive Test Cases:")
    print(result["positive_test_cases"])
    print("\nNegative Test Cases:")
    print(result["negative_test_cases"])

if __name__ == "__main__":
    main() 