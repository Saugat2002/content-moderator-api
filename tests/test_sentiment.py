import pytest
from app.services.sentiment import SentimentAnalyzer


@pytest.fixture
def sentiment_analyzer():
    return SentimentAnalyzer()


def test_sentiment_analyzer_initialization(sentiment_analyzer):
    """Test if sentiment analyzer initializes correctly"""
    assert sentiment_analyzer is not None
    assert sentiment_analyzer.model is not None
    assert sentiment_analyzer.tokenizer is not None


def test_analyze_sentiment_structure(sentiment_analyzer):
    """Test if sentiment analysis returns correct structure"""
    text = "I love this product!"
    result = sentiment_analyzer.analyze_sentiment(text)

    assert isinstance(result, dict)
    assert "sentiment_score" in result
    assert "confidence" in result
    assert "dominant_emotion" in result
    assert "raw_scores" in result

    assert isinstance(result["sentiment_score"], float)
    assert isinstance(result["confidence"], float)
    assert isinstance(result["dominant_emotion"], str)
    assert isinstance(result["raw_scores"], dict)


def test_sentiment_score_range(sentiment_analyzer):
    """Test if sentiment score is within expected range"""
    text = "I love this product!"
    result = sentiment_analyzer.analyze_sentiment(text)
    assert -1 <= result["sentiment_score"] <= 1


def test_confidence_range(sentiment_analyzer):
    """Test if confidence score is within expected range"""
    text = "I love this product!"
    result = sentiment_analyzer.analyze_sentiment(text)
    assert 0 <= result["confidence"] <= 1


def test_positive_sentiment(sentiment_analyzer):
    """Test positive sentiment analysis"""
    text = "I love this product! It's amazing!"
    result = sentiment_analyzer.analyze_sentiment(text)
    assert result["sentiment_score"] > 0
    assert result["dominant_emotion"] in ["joy", "love", "excitement"]


def test_negative_sentiment(sentiment_analyzer):
    """Test negative sentiment analysis"""
    text = "I hate this product! It's terrible!"
    result = sentiment_analyzer.analyze_sentiment(text)
    assert result["sentiment_score"] < 0
    assert result["dominant_emotion"] in ["anger", "disappointment", "disgust"]


def test_neutral_sentiment(sentiment_analyzer):
    """Test neutral sentiment analysis"""
    text = "Today is Sunday"
    result = sentiment_analyzer.analyze_sentiment(text)
    assert abs(result["sentiment_score"]) < 0.3
    assert result["dominant_emotion"] == "neutral"


def test_special_characters(sentiment_analyzer):
    """Test handling of special characters"""
    text = "Hello! @#$%^&*()"
    result = sentiment_analyzer.analyze_sentiment(text)
    assert isinstance(result, dict)
    assert "sentiment_score" in result


def test_get_sentiment_label(sentiment_analyzer):
    """Test sentiment label mapping"""
    assert sentiment_analyzer.get_sentiment_label(0.8) in ["positive", "very_positive"]
    assert sentiment_analyzer.get_sentiment_label(-0.8) in ["negative", "very_negative"]
    assert sentiment_analyzer.get_sentiment_label(0.1) == "neutral"
    assert sentiment_analyzer.get_sentiment_label(-0.1) == "neutral"
