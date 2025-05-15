import pytest
from app.services.moderation import ModerationService
from app.services.cache import CacheService
from app.core.config import get_settings

settings = get_settings()


@pytest.fixture
def cache_service():
    return CacheService()


@pytest.fixture
def moderation_service(cache_service):
    return ModerationService(cache_service)


@pytest.mark.asyncio
async def test_moderation_service_initialization(moderation_service):
    """Test if moderation service initializes correctly"""
    assert moderation_service is not None
    assert moderation_service.sentiment_analyzer is not None
    assert moderation_service.cache_service is not None


@pytest.mark.asyncio
async def test_analyze_text_structure(moderation_service):
    """Test if text analysis returns correct structure"""
    text = "I love this product!"
    result = await moderation_service.analyze_text(text)

    assert isinstance(result, dict)
    assert "sentiment_score" in result
    assert "sentiment" in result
    assert "confidence" in result
    assert "dominant_emotion" in result
    assert "raw_scores" in result

    assert isinstance(result["sentiment_score"], float)
    assert isinstance(result["sentiment"], str)
    assert isinstance(result["confidence"], float)
    assert isinstance(result["dominant_emotion"], str)
    assert isinstance(result["raw_scores"], dict)


@pytest.mark.asyncio
async def test_analyze_text_caching(moderation_service):
    """Test if text analysis results are cached"""
    text = "This is a test message"

    # First analysis
    result1 = await moderation_service.analyze_text(text)

    # Second analysis (should use cache)
    result2 = await moderation_service.analyze_text(text)

    assert result1 == result2


@pytest.mark.asyncio
async def test_analyze_text_positive(moderation_service):
    """Test positive text analysis"""
    text = "I love this product! It's amazing!"
    result = await moderation_service.analyze_text(text)

    assert result["sentiment_score"] > 0
    assert result["sentiment"] in ["positive", "very_positive"]
    assert result["confidence"] > 0.5


@pytest.mark.asyncio
async def test_analyze_text_negative(moderation_service):
    """Test negative text analysis"""
    text = "I hate this product! It's terrible!"
    result = await moderation_service.analyze_text(text)

    assert result["sentiment_score"] < 0
    assert result["sentiment"] in ["negative", "very_negative"]
    assert result["confidence"] > 0.5


@pytest.mark.asyncio
async def test_analyze_text_neutral(moderation_service):
    """Test neutral text analysis"""
    text = "Today is Sunday"
    result = await moderation_service.analyze_text(text)

    assert abs(result["sentiment_score"]) < 0.3
    assert result["sentiment"] in ["neutral"]
    assert result["confidence"] > 0.5


@pytest.mark.asyncio
async def test_analyze_text_empty(moderation_service):
    """Test handling of empty text"""
    result = await moderation_service.analyze_text("")

    # Empty text should return neutral sentiment
    assert isinstance(result, dict)
    assert result["sentiment"] == "neutral"
    assert result["confidence"] > 0.0


@pytest.mark.asyncio
async def test_analyze_text_long(moderation_service):
    """Test handling of long text"""
    long_text = "This is a test sentence with multiple words. " * 8
    result = await moderation_service.analyze_text(long_text)

    # Verify that we get a valid response
    assert isinstance(result, dict)
    assert "sentiment_score" in result
    assert "sentiment" in result
    assert "confidence" in result
    assert "dominant_emotion" in result
    assert "raw_scores" in result

    # Verify the response structure is valid
    assert isinstance(result["sentiment_score"], float)
    assert isinstance(result["sentiment"], str)
    assert isinstance(result["confidence"], float)
    assert isinstance(result["dominant_emotion"], str)
    assert isinstance(result["raw_scores"], dict)

    # Verify the scores are within valid ranges
    assert -1 <= result["sentiment_score"] <= 1
    assert 0 <= result["confidence"] <= 1


@pytest.mark.asyncio
async def test_analyze_text_special_chars(moderation_service):
    """Test handling of special characters"""
    text = "Hello! @#$%^&*()"
    result = await moderation_service.analyze_text(text)

    assert isinstance(result, dict)
    assert "sentiment_score" in result
    assert "sentiment" in result


@pytest.mark.asyncio
async def test_analyze_text_emotions(moderation_service):
    """Test emotion detection in text"""
    text = "I am so angry and disappointed!"
    result = await moderation_service.analyze_text(text)

    assert "raw_scores" in result
    assert isinstance(result["raw_scores"], dict)
    assert len(result["raw_scores"]) > 0
    assert result["dominant_emotion"] in ["anger", "disappointment"]


@pytest.mark.asyncio
async def test_cache_service(cache_service):
    # Test setting and getting from cache
    await cache_service.set("test_key", {"test": "value"})
    result = await cache_service.get("test_key")
    assert result == {"test": "value"}

    # Test cache miss
    result = await cache_service.get("nonexistent_key")
    assert result is None

    # Test cache deletion
    await cache_service.delete("test_key")
    result = await cache_service.get("test_key")
    assert result is None

    # Test cache clear
    await cache_service.set("key1", "value1")
    await cache_service.set("key2", "value2")
    await cache_service.clear()
    assert await cache_service.get("key1") is None
    assert await cache_service.get("key2") is None
