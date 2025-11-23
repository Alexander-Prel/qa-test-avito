import pytest
import requests
import random
import time

BASE_URL = "https://qa-internship.avito.com"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def session():
    return requests.Session()


@pytest.fixture
def unique_seller_id():
    timestamp_part = int(time.time()) % 10000
    random_part = random.randint(111111, 999999)
    seller_id = (random_part + timestamp_part) % 888888 + 111111
    return seller_id


@pytest.fixture
def sample_ad_data(unique_seller_id):
    return {
        "sellerID": unique_seller_id,
        "name": "Тестовое объявление",
        "price": 1000,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        }
    }


@pytest.fixture
def created_ad(session, base_url, sample_ad_data):
    response = session.post(f"{base_url}/api/1/item", json=sample_ad_data)
    if response.status_code == 200:
        response_data = response.json()
        seller_id = sample_ad_data["sellerID"]
        get_response = session.get(f"{base_url}/api/1/{seller_id}/item")
        if get_response.status_code == 200:
            ads = get_response.json()
            if ads and len(ads) > 0:
                ad_data = ads[-1]
                yield ad_data
            else:
                pytest.skip("Не удалось получить созданное объявление")
        else:
            pytest.skip(f"Не удалось получить созданное объявление: {get_response.status_code}")
    else:
        pytest.skip(f"Не удалось создать тестовое объявление: {response.status_code}, ответ: {response.text}")


@pytest.fixture
def multiple_ads(session, base_url, unique_seller_id):
    created_count = 0
    for i in range(3):
        ad_data = {
            "sellerID": unique_seller_id,
            "name": f"Объявление {i+1}",
            "price": 1000 + i * 100,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }
        response = session.post(f"{base_url}/api/1/item", json=ad_data)
        if response.status_code == 200:
            created_count += 1
        time.sleep(0.1)
    
    get_response = session.get(f"{base_url}/api/1/{unique_seller_id}/item")
    if get_response.status_code == 200:
        ads = get_response.json()
        yield ads[-created_count:] if len(ads) >= created_count else ads
    else:
        yield []

