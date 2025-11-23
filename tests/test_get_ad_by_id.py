import pytest
import requests


class TestGetAdById:

    def test_get_existing_ad(self, session, base_url, created_ad):
        ad_id = created_ad["id"]
        response = session.get(f"{base_url}/api/1/item/{ad_id}")
        
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        
        data = response.json()
        if isinstance(data, list):
            assert len(data) > 0, "Массив объявлений не должен быть пустым"
            ad = data[0]
        else:
            ad = data
        
        assert "id" in ad, "В ответе отсутствует поле 'id'"
        assert str(ad["id"]) == str(ad_id), "ID в ответе не совпадает с запрошенным"
        assert "name" in ad, "В ответе отсутствует поле 'name'"
        assert "price" in ad, "В ответе отсутствует поле 'price'"
        assert "sellerId" in ad or "sellerID" in ad, "В ответе отсутствует поле 'sellerId'"

    def test_get_nonexistent_ad(self, session, base_url):
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        response = session.get(f"{base_url}/api/1/item/{nonexistent_id}")
        
        assert response.status_code in [400, 404], \
            f"Ожидался статус 400 или 404, получен {response.status_code}. Ответ: {response.text}"

    def test_get_ad_invalid_id_format(self, session, base_url):
        invalid_id = "abc"
        response = session.get(f"{base_url}/api/1/item/{invalid_id}")
        
        assert response.status_code in [400, 404], \
            f"Ожидался статус 400 или 404, получен {response.status_code}. Ответ: {response.text}"

    def test_get_ad_data_persistence(self, session, base_url, sample_ad_data):
        create_response = session.post(f"{base_url}/api/1/item", json=sample_ad_data)
        assert create_response.status_code == 200, f"Не удалось создать объявление: {create_response.status_code}, {create_response.text}"
        
        seller_id = sample_ad_data["sellerID"]
        get_seller_response = session.get(f"{base_url}/api/1/{seller_id}/item")
        assert get_seller_response.status_code == 200, "Не удалось получить объявления продавца"
        seller_ads = get_seller_response.json()
        
        created_ad = None
        for ad in seller_ads:
            if ad.get("name") == sample_ad_data["name"]:
                created_ad = ad
                break
        
        assert created_ad is not None, "Созданное объявление не найдено"
        ad_id = created_ad["id"]
        
        get_response = session.get(f"{base_url}/api/1/item/{ad_id}")
        assert get_response.status_code == 200, f"Не удалось получить объявление: {get_response.status_code}, {get_response.text}"
        retrieved_data = get_response.json()
        
        if isinstance(retrieved_data, list):
            assert len(retrieved_data) > 0, "Массив объявлений не должен быть пустым"
            retrieved_ad = retrieved_data[0]
        else:
            retrieved_ad = retrieved_data
        
        seller_id_retrieved = retrieved_ad.get("sellerId") or retrieved_ad.get("sellerID")
        assert seller_id_retrieved == sample_ad_data["sellerID"], \
            f"sellerId не совпадает: ожидалось {sample_ad_data['sellerID']}, получено {seller_id_retrieved}"
        assert retrieved_ad.get("name") == sample_ad_data["name"], \
            f"name не совпадает: ожидалось {sample_ad_data['name']}, получено {retrieved_ad.get('name')}"
        assert retrieved_ad.get("price") == sample_ad_data["price"], \
            f"price не совпадает: ожидалось {sample_ad_data['price']}, получено {retrieved_ad.get('price')}"

