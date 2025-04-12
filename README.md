# Test Case Generation System

A comprehensive system for generating test cases using AI, combining a Python backend with a React frontend.

## Author

**Anurag Pathak**

## Project Structure

```
.
├── frontend/          # React frontend application
│   ├── src/          # Source files
│   ├── public/       # Static files
│   └── package.json  # Frontend dependencies
├── app.py            # Flask backend server
├── test_case_agent.py # Test case generation logic
├── config.py         # Configuration settings
└── main.py           # Main application entry point
```

## Features

- AI-powered test case generation
- Positive and negative test case creation
- Interactive web interface
- RESTful API endpoints
- Integration with Qdrant for vector storage

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- OpenAI API key
- Qdrant instance

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your environment variables:
```
OPENAI_API_KEY=your_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## Running the Application

1. Start the backend server:
```bash
python app.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

The application will be available at `http://localhost:3000`

## API Endpoints

- `POST /api/generate-test-cases`: Generate test cases based on input criteria

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the GPT models
- Qdrant for vector storage
- Flask and React communities 