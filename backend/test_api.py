#!/usr/bin/env python3
"""
Test script for the Digital Signage API
"""

import asyncio
import httpx
from app.core.config import settings

BASE_URL = f"http://{settings.API_HOST}:{settings.API_PORT}{settings.API_V1_STR}"

async def test_api():
    """Test the API endpoints"""
    async with httpx.AsyncClient() as client:
        print("Testing Digital Signage API...")
        print(f"Base URL: {BASE_URL}")

        # Test health check
        try:
            response = await client.get(f"{BASE_URL.replace('/api/v1', '')}/health")
            print(f"Health check: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Health check failed: {e}")

        # Test API docs
        try:
            response = await client.get(f"{BASE_URL.replace('/api/v1', '')}/docs")
            print(f"API docs: {response.status_code}")
        except Exception as e:
            print(f"API docs failed: {e}")

        print("API test completed!")

if __name__ == "__main__":
    asyncio.run(test_api())
