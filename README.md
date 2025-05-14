# AI-Powered Content Moderator API

A FastAPI-based content moderation service that analyzes text for toxicity and sentiment using AI models. The service includes a web interface for easy interaction and follows 12-Factor principles for cloud-native deployment.

## Features

- **Text Analysis**
  - Toxicity detection
  - Sentiment analysis
  - Configurable moderation thresholds
  - Real-time analysis results

- **Web Interface**
  - User-friendly dashboard
  - Visual score representation
  - Real-time analysis feedback
  - Responsive design

- **Technical Features**
  - FastAPI framework
  - Redis caching
  - API key authentication
  - Comprehensive logging
  - Docker support
  - CI/CD pipeline
  - Type hints and validation
  - Pre-commit hooks

## Prerequisites

- Python 3.11+
- Redis server
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd content-moderator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

### Development Mode

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. Access the web interface:
- Open http://localhost:8000 in your browser
- Enter your API key and text to analyze
- View real-time analysis results

3. API Documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t content-moderator .
```

2. Run the container:
```bash
docker run -p 8000:8000 content-moderator
```

## Testing

### Running Tests

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Run the test suite:
```bash
pytest -v
```

### Code Quality

1. Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

2. Run linting:
```bash
black .
mypy .
```

## API Usage

### Authentication

All API requests require an API key in the `X-API-Key` header.

### Endpoints

- `POST /api/v1/analyze`
  - Analyzes text for toxicity and sentiment
  - Request body: `{"text": "string"}`
  - Response: Analysis results with toxicity and sentiment scores

## Web Interface

The web interface provides:
- Text input area for content analysis
- API key authentication
- Visual representation of analysis results:
  - Toxicity score bar
  - Sentiment score bar
  - Overall sentiment classification
  - Color-coded results

## Development

### Project Structure

```
content-moderator/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── services/
│   │   ├── moderation.py
│   │   └── cache.py
│   ├── templates/
│   │   └── index.html
│   └── main.py
├── tests/
│   └── test_moderation.py
├── .env.example
├── .pre-commit-config.yaml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```
