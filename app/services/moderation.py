from typing import Dict, Any, cast
import logging
from .sentiment import SentimentAnalyzer
from .cache import CacheService

logger = logging.getLogger(__name__)


class ModerationService:
    def __init__(self, cache_service: CacheService):
        self.cache_service = cache_service
        self.sentiment_analyzer = SentimentAnalyzer()
        logger.info("Initialized ModerationService")

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for sentiment and toxicity using BERT.
        """
        try:
            # Check cache first
            cache_key = f"analysis:{text}"
            cached_result = await self.cache_service.get(cache_key)
            if cached_result:
                logger.info("Retrieved analysis from cache")
                return cached_result

            # Perform sentiment analysis
            sentiment_result = self.sentiment_analyzer.analyze_sentiment(text)

            sentiment_score: float = cast(float, sentiment_result["sentiment_score"])

            # Prepare response
            result = {
                "sentiment_score": sentiment_score,
                "sentiment": self.sentiment_analyzer.get_sentiment_label(
                    sentiment_score
                ),
                "confidence": sentiment_result["confidence"],
                "raw_scores": sentiment_result["raw_scores"],
            }

            # Cache the result
            await self.cache_service.set(cache_key, result)
            logger.info("Analysis completed and cached")

            return result

        except Exception as e:
            logger.error(f"Error in text analysis: {str(e)}")
            raise
