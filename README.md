# AI-Powered Content Moderator API

A FastAPI-based microservice that analyzes text content for toxicity, profanity, and sentiment, helping content platforms maintain healthy online environments.

## Features

- Text analysis endpoints for toxicity detection, sentiment analysis, and content categorization
- Configurable moderation thresholds via environment variables
- Rate limiting and API key authentication
- Comprehensive logging of moderation decisions
- Redis caching layer for improved performance

## Project Structure

```
.
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── moderation.py
│   │   └── cache.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_moderation.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Redis (handled by Docker Compose)

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
API_KEY=your_api_key_here
MODEL_THRESHOLD=0.7
REDIS_URL=redis://redis:6379/0
```

## Running Locally

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Running with Docker

1. Build and start the containers:
```bash
docker-compose up --build
```

2. The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run tests using pytest:
```bash
pytest
```

## Development

- The project uses pre-commit hooks for code quality
- GitHub Actions workflow for CI/CD
- Code formatting with black
- Type checking with mypy

## License

MIT
