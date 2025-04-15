from flask import Flask, request, jsonify
from flask_cors import CORS
from test_case_agent import process_input
from config import JsonData
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/generate-test-cases', methods=['POST'])
def generate_test_cases():
    try:
        data = request.json
        pbi = data.get('pbi', '')
        additional_details = data.get('additional_details', '')
        
        # Process the input using the existing agent
        result = process_input(
            pbi=pbi,
            additional_details=additional_details,
            positive_test_cases=JsonData.POSITIVE_TEST_CASES_EXAMPLE,
            negative_test_cases=JsonData.NEGATIVE_TEST_CASES_EXAMPLE
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 