import pytest
from app.services.moderation import ModerationService
from app.services.cache import CacheService
from app.core.config import get_settings

settings = get_settings()


@pytest.fixture
def moderation_service():
    return ModerationService()


@pytest.fixture
def cache_service():
    return CacheService()


@pytest.mark.asyncio
async def test_analyze_text_positive(moderation_service):
    text = "This is a great and wonderful day!"
    result = await moderation_service.analyze_text(text)

    assert result["toxicity_score"] < 0.5
    assert not result["is_toxic"]
    assert result["sentiment_score"] > 0.5
    assert result["sentiment"] == "positive"


@pytest.mark.asyncio
async def test_analyze_text_negative(moderation_service):
    text = "This is terrible, awful, bad and I hate it!"
    result = await moderation_service.analyze_text(text)

    assert result["toxicity_score"] > 0.3
    # assert result["is_toxic"]
    assert result["sentiment_score"] < 0.3
    assert result["sentiment"] == "negative"


@pytest.mark.asyncio
async def test_analyze_text_neutral(moderation_service):
    text = "The weather is cloudy today."
    result = await moderation_service.analyze_text(text)

    assert result["toxicity_score"] < 0.5
    assert not result["is_toxic"]
    assert 0.3 <= result["sentiment_score"] <= 0.5
    assert result["sentiment"] == "neutral"


@pytest.mark.asyncio
async def test_analyze_text_empty(moderation_service):
    text = ""
    result = await moderation_service.analyze_text(text)

    assert result["toxicity_score"] == 0.0
    assert not result["is_toxic"]
    assert result["sentiment_score"] == 0.5
    assert result["sentiment"] == "neutral"


@pytest.mark.asyncio
async def test_analyze_text_mixed(moderation_service):
    text = "This is both great and terrible!"
    result = await moderation_service.analyze_text(text)

    assert result["toxicity_score"] > 0.0
    assert result["sentiment_score"] > 0.0
    assert result["sentiment_score"] < 1.0


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
