from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from typing import Dict, Any
from app.core.security import get_api_key
from app.services.moderation import ModerationService
from app.services.cache import CacheService
from app.core.config import get_settings
import logging

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


class TextAnalysisRequest(BaseModel):
    text: str


class TextAnalysisResponse(BaseModel):
    sentiment_score: float
    sentiment: str
    confidence: float
    dominant_emotion: str
    raw_scores: Dict[str, float]


async def get_moderation_service() -> ModerationService:
    cache_service = CacheService()
    return ModerationService(cache_service)


async def verify_api_key(x_api_key: str = Header(...)) -> None:
    if x_api_key != settings.API_KEY:
        logger.warning("Invalid API key attempt")
        raise HTTPException(status_code=401, detail="Invalid API key")


@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest,
    moderation_service: ModerationService = Depends(get_moderation_service),
    _: None = Depends(verify_api_key),
) -> Dict[str, Any]:
    """
    Analyze text for sentiment and emotions using BERT.
    """
    try:
        result = await moderation_service.analyze_text(request.text)
        # Ensure sentiment field is present
        if "sentiment" not in result:
            result["sentiment"] = "neutral"  # Default sentiment if not provided
        return result
    except Exception as e:
        logger.error(f"Error in analyze_text endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
