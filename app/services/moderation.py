from typing import Dict, Any
import httpx
from app.core.config import get_settings

settings = get_settings()


class ModerationService:
    def __init__(self):
        self.threshold = settings.MODEL_THRESHOLD
        self.positive_words = settings.POSITIVE_WORDS
        self.negative_words = settings.NEGATIVE_WORDS
        self.toxic_words = settings.TOXIC_WORDS

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for toxicity and sentiment.
        This is a simplified version that could be replaced with a real AI service.
        """
        # Simulate AI analysis
        # In a real implementation, this would call an external AI service
        toxicity_score = self._calculate_toxicity(text)
        sentiment_score = self._calculate_sentiment(text)

        return {
            "toxicity_score": toxicity_score,
            "is_toxic": toxicity_score > self.threshold,
            "sentiment_score": sentiment_score,
            "sentiment": (
                "positive"
                if sentiment_score > 0.5
                else "negative"
                if sentiment_score < 0.3
                else "neutral"
            ),
        }

    def _calculate_toxicity(self, text: str) -> float:
        """
        Calculate toxicity score based on predefined toxic words.
        """
        text_lower = text.lower()
        score = sum(1 for word in self.toxic_words if word in text_lower) / len(
            self.toxic_words
        )
        return min(score, 1.0)

    def _calculate_sentiment(self, text: str) -> float:
        """
        Calculate sentiment score based on predefined positive and negative words.
        """
        text_lower = text.lower()
        positive_score = sum(1 for word in self.positive_words if word in text_lower)
        negative_score = sum(1 for word in self.negative_words if word in text_lower)

        total = positive_score + negative_score
        if total == 0:
            return 0.5  # neutral

        return positive_score / total
