import pytest
import aiohttp
import time

BASE_URL = "http://127.0.0.1:5000"

@pytest.mark.asyncio
async def test_system_post_measurement_succes():
    """Tes 1: Sprawdzenie poprawnego zapisu pomiaru pacjenta"""
    url=f"{BASE_URL}/api/measurements"
    now = time.time()
    payload = {
        "patient_id": "patient_001",
        "source_time": now,
        "value": 75,
        "stream_time": now
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            assert response.status in (200, 201), f"Serwer zwrócił zły status: {response.status}"
            data = await response.json()
            assert data is not None

@pytest.mark.asyncio
async def test_system_post_measurement_bad_data():
    """Test 2: Sprawdzenie odporności na błędne dane"""     
    url=f"{BASE_URL}/api/measurements"
    now = time.time()
    payload = {
        "patient_id": "patient_002",
        "source_time": now,
        "value": "not_a_number",
        "stream_time": now
    }    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            assert response.status not in (200, 201), f"Serwer nie powinien akceptować błędnych danych, ale zwrócił status: {response.status}"
 