import pytest
from fastapi import HTTPException
from app.core.security import get_api_key
from app.core.config import get_settings

settings = get_settings()


@pytest.mark.asyncio
async def test_get_api_key_valid():
    """Test getting API key with valid key"""
    api_key = settings.API_KEY
    result = await get_api_key(api_key)
    assert result == api_key


@pytest.mark.asyncio
async def test_get_api_key_invalid():
    """Test getting API key with invalid key"""
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key("invalid_key")

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Could not validate API key"


@pytest.mark.asyncio
async def test_get_api_key_empty():
    """Test getting API key with empty key"""
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key("")

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Could not validate API key"


@pytest.mark.asyncio
async def test_get_api_key_none():
    """Test getting API key with None"""
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(None)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Could not validate API key"
