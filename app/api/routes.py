from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
from app.core.security import get_api_key
from app.services.moderation import ModerationService
from app.services.cache import CacheService
import hashlib

router = APIRouter()
moderation_service = ModerationService()
cache_service = CacheService()


class TextAnalysisRequest(BaseModel):
    text: str


class TextAnalysisResponse(BaseModel):
    toxicity_score: float
    is_toxic: bool
    sentiment_score: float
    sentiment: str


@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest, api_key: str = Depends(get_api_key)
) -> Dict[str, Any]:
    """
    Analyze text for toxicity and sentiment.
    """
    # Generate cache key from text
    cache_key = f"analysis:{hashlib.md5(request.text.encode()).hexdigest()}"

    # Try to get from cache first
    cached_result = await cache_service.get(cache_key)
    if cached_result:
        return cached_result

    # If not in cache, analyze text
    result = await moderation_service.analyze_text(request.text)

    # Cache the result
    await cache_service.set(cache_key, result)

    return result


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
