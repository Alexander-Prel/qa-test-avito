import pytest
import requests


class TestCreateAd:

    def test_create_ad_success(self, session, base_url, sample_ad_data):
        response = session.post(f"{base_url}/api/1/item", json=sample_ad_data)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        response_data = response.json()
        
        seller_id = sample_ad_data["sellerID"]
        get_response = session.get(f"{base_url}/api/1/{seller_id}/item")
        assert get_response.status_code == 200, "Не удалось получить объявления продавца"
        ads = get_response.json()
        
        created_ad = None
        for ad in ads:
            seller_id_in_ad = ad.get("sellerId") or ad.get("sellerID")
            if seller_id_in_ad == seller_id and ad.get("name") == sample_ad_data["name"]:
                created_ad = ad
                break
        
        assert created_ad is not None, "Созданное объявление не найдено в списке объявлений продавца"
        assert "id" in created_ad, "В ответе отсутствует поле 'id'"
        assert isinstance(created_ad["id"], (int, str)), "Поле 'id' должно быть числом или строкой"
        
        assert created_ad.get("name") == sample_ad_data["name"]
        assert created_ad.get("price") == sample_ad_data["price"]

    def test_create_ad_missing_required_fields(self, session, base_url, unique_seller_id):
        incomplete_data = {
            "sellerID": unique_seller_id,
            "price": 1000
        }
        response = session.post(f"{base_url}/api/1/item", json=incomplete_data)
        
        assert response.status_code in [400, 422], \
            f"Ожидался статус 400 или 422, получен {response.status_code}. Ответ: {response.text}"

    def test_create_ad_invalid_price_type(self, session, base_url, unique_seller_id):
        invalid_data = {
            "sellerID": unique_seller_id,
            "name": "Тест",
            "price": "не число"
        }
        response = session.post(f"{base_url}/api/1/item", json=invalid_data)
        
        assert response.status_code in [400, 422], \
            f"Ожидался статус 400 или 422, получен {response.status_code}. Ответ: {response.text}"

    def test_create_ad_negative_price(self, session, base_url, unique_seller_id):
        invalid_data = {
            "sellerID": unique_seller_id,
            "name": "Тест",
            "price": -100
        }
        response = session.post(f"{base_url}/api/1/item", json=invalid_data)
        
        assert response.status_code in [400, 422], \
            f"Ожидался статус 400 или 422, получен {response.status_code}. Ответ: {response.text}"

    def test_create_ad_empty_name(self, session, base_url, unique_seller_id):
        invalid_data = {
            "sellerID": unique_seller_id,
            "name": "",
            "price": 1000
        }
        response = session.post(f"{base_url}/api/1/item", json=invalid_data)
        
        assert response.status_code in [400, 422, 200], \
            f"Неожиданный статус код: {response.status_code}. Ответ: {response.text}"

    def test_create_ad_unique_ids(self, session, base_url, unique_seller_id):
        for i in range(3):
            ad_data = {
                "sellerID": unique_seller_id,
                "name": f"Тест {i}",
                "price": 1000,
                "statistics": {
                    "likes": 1,
                    "viewCount": 1,
                    "contacts": 1
                }
            }
            response = session.post(f"{base_url}/api/1/item", json=ad_data)
            assert response.status_code == 200, f"Не удалось создать объявление {i}"
        
        get_response = session.get(f"{base_url}/api/1/{unique_seller_id}/item")
        assert get_response.status_code == 200
        ads = get_response.json()
        
        ids = [ad["id"] for ad in ads if ad.get("name", "").startswith("Тест")]
        assert len(ids) == len(set(ids)), f"Найдены дублирующиеся ID: {ids}"

