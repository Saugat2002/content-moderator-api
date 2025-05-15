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
        Analyze text for sentiment and emotions using BERT.
        """
        try:
            # Check cache first
            cache_key = f"analysis:{text}"
            cached_result = await self.cache_service.get(cache_key)
            if cached_result:
                logger.info("Retrieved analysis from cache")
                return cached_result

            # Perform sentiment analysis
            analysis_result = self.sentiment_analyzer.analyze_sentiment(text)

            sentiment_score: float = cast(float, analysis_result["sentiment_score"])
            confidence: float = cast(float, analysis_result["confidence"])
            dominant_emotion: str = cast(str, analysis_result["dominant_emotion"])
            raw_scores: Dict[str, float] = cast(
                Dict[str, float], analysis_result["raw_scores"]
            )

            # Prepare response
            result = {
                "sentiment_score": sentiment_score,
                "confidence": confidence,
                "dominant_emotion": dominant_emotion,
                "raw_scores": raw_scores,
            }

            # Cache the result
            await self.cache_service.set(cache_key, result)
            logger.info("Analysis completed and cached")

            return result

        except Exception as e:
            logger.error(f"Error in text analysis: {str(e)}")
            raise
