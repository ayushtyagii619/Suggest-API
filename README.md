# Suggestor_API

A Django REST API that analyzes text messages using gemini-1.5-pro-latest to determine tone and intent, then suggests relevant actions.

## Features

- Analyzes text messages for tone and intent
- Suggests relevant actions based on analysis
- Logs all requests to PostgreSQL database
- Single API endpoint for analysis

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/action-suggester-api.git
   cd action-suggester-api

2. Create and activate a virtual environment:
   python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Create a .env file in the project root with your OpenAI API key:
   LLM_API_KEY=your_openai_api_key_here

5.Configure PostgreSQL:
  Create a PostgreSQL database
  Update the database settings in settings.py:
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

6. Run migrations:
   python manage.py migrate

7. Start the development server:
   python manage.py runserver


# API Endpoint
## Analyze Text
  Endpoint: POST /api/analyze/
  Request Body:
  {
    "query": "Your text message here"
}
## Success Response:
  {
    "id": 1,
    "query": "I want to order pizza",
    "tone": "Happy",
    "intent": "Order Food",
    "suggested_actions": [
        {"action_code": "ORDER_FOOD", "display_text": "Order Food Online"}
    ],
    "timestamp": "2023-12-01T12:00:00Z"
}


# Testing with Postman
  1. Import the Postman collection (if available)
  2. Send a POST request to http://localhost:8000/api/analyze/
  3. Set the Content-Type header to application/json
  4. Include the request body as shown above

# Environment Variables
  LLM_API_KEY: Your OpenAI API key (required)

# LLM Provider
This project uses gemini-1.5-pro-latest for text analysis.
