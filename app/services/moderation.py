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
            logger.info(f"Analyzing text: {text[:50]}...")  # Log first 50 chars of text

            # Check cache first
            cache_key = f"analysis:{text}"
            cached_result = await self.cache_service.get(cache_key)
            if cached_result:
                logger.info("Retrieved analysis from cache")
                return cached_result

            # Perform sentiment analysis
            logger.info("Performing sentiment analysis")
            analysis_result = self.sentiment_analyzer.analyze_sentiment(text)
            logger.debug(f"Raw analysis result: {analysis_result}")

            # Get sentiment label
            sentiment_label = self.sentiment_analyzer.get_sentiment_label(
                cast(float, analysis_result["sentiment_score"])
            )
            logger.info(f"Detected sentiment: {sentiment_label}")

            # Prepare response
            result = {
                "sentiment_score": analysis_result["sentiment_score"],
                "sentiment": sentiment_label,
                "confidence": analysis_result["confidence"],
                "dominant_emotion": analysis_result["dominant_emotion"],
                "raw_scores": analysis_result["raw_scores"],
            }
            logger.debug(f"Prepared response: {result}")

            # Cache the result
            await self.cache_service.set(cache_key, result)
            logger.info("Analysis completed and cached")

            return result

        except Exception as e:
            logger.error(f"Error in text analysis: {str(e)}", exc_info=True)
            raise
