import sys
import os
from pathlib import Path
import pytest

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now import the app modules after path is set
from app.services.sentiment import SentimentAnalyzer
from app.services.moderation import ModerationService
from app.services.cache import CacheService


@pytest.fixture
def sentiment_analyzer():
    return SentimentAnalyzer()


@pytest.fixture
def cache_service():
    return CacheService()


@pytest.fixture
def moderation_service(cache_service):
    return ModerationService(cache_service)
