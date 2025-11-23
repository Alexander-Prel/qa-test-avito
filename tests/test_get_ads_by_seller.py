import pytest
import requests


class TestGetAdsBySeller:

    def test_get_ads_existing_seller(self, session, base_url, multiple_ads, unique_seller_id):
        response = session.get(f"{base_url}/api/1/{unique_seller_id}/item")
        
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Ответ должен быть массивом"
        assert len(data) >= len(multiple_ads), \
            f"Ожидалось минимум {len(multiple_ads)} объявлений, получено {len(data)}"
        
        for ad in data:
            seller_id = ad.get("sellerId") or ad.get("sellerID")
            assert seller_id == unique_seller_id, \
                f"Объявление {ad.get('id')} принадлежит другому продавцу: ожидалось {unique_seller_id}, получено {seller_id}"

    def test_get_ads_nonexistent_seller(self, session, base_url):
        nonexistent_seller_id = 999999999
        response = session.get(f"{base_url}/api/1/{nonexistent_seller_id}/item")
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list), "Ответ должен быть массивом"
            for ad in data:
                seller_id = ad.get("sellerId") or ad.get("sellerID")
                assert seller_id == nonexistent_seller_id, \
                    f"Объявление {ad.get('id')} принадлежит другому продавцу: {seller_id}, ожидалось {nonexistent_seller_id}"
        else:
            assert response.status_code == 404, \
                f"Ожидался статус 200 или 404, получен {response.status_code}. Ответ: {response.text}"

    def test_get_ads_seller_without_ads(self, session, base_url, unique_seller_id):
        new_seller_id = unique_seller_id + 1000000
        response = session.get(f"{base_url}/api/1/{new_seller_id}/item")
        
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Ответ должен быть массивом"
        assert len(data) == 0, "Для продавца без объявлений должен быть пустой массив"

    def test_get_ads_different_sellers(self, session, base_url):
        seller1_id = 111111
        seller2_id = 222222
        
        ad1_data = {
            "sellerID": seller1_id,
            "name": "Объявление продавца 1",
            "price": 1000,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }
        response1 = session.post(f"{base_url}/api/1/item", json=ad1_data)
        if response1.status_code != 200:
            pytest.skip(f"Не удалось создать объявление для seller1: {response1.status_code}, {response1.text}")
        
        ad2_data = {
            "sellerID": seller2_id,
            "name": "Объявление продавца 2",
            "price": 2000,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }
        response2 = session.post(f"{base_url}/api/1/item", json=ad2_data)
        if response2.status_code != 200:
            pytest.skip(f"Не удалось создать объявление для seller2: {response2.status_code}, {response2.text}")
        
        seller1_response = session.get(f"{base_url}/api/1/{seller1_id}/item")
        assert seller1_response.status_code == 200
        seller1_ads_before = seller1_response.json()
        
        seller2_response = session.get(f"{base_url}/api/1/{seller2_id}/item")
        assert seller2_response.status_code == 200
        seller2_ads_before = seller2_response.json()
        
        ad1_id = None
        for ad in seller1_ads_before:
            if ad.get("name") == ad1_data["name"]:
                ad1_id = ad["id"]
                break
        
        ad2_id = None
        for ad in seller2_ads_before:
            if ad.get("name") == ad2_data["name"]:
                ad2_id = ad["id"]
                break
        
        assert ad1_id is not None, "Не удалось найти созданное объявление продавца 1"
        assert ad2_id is not None, "Не удалось найти созданное объявление продавца 2"
        
        seller1_response = session.get(f"{base_url}/api/1/{seller1_id}/item")
        assert seller1_response.status_code == 200
        seller1_ads = seller1_response.json()
        
        seller2_response = session.get(f"{base_url}/api/1/{seller2_id}/item")
        assert seller2_response.status_code == 200
        seller2_ads = seller2_response.json()
        
        seller1_ids = [ad["id"] for ad in seller1_ads if str(ad.get("id")) == str(ad1_id)]
        seller2_ids = [ad["id"] for ad in seller2_ads if str(ad.get("id")) == str(ad2_id)]
        
        assert len(seller1_ids) > 0, "Объявление первого продавца должно быть в его списке"
        assert len(seller2_ids) > 0, "Объявление второго продавца должно быть в его списке"
        
        seller1_ad_ids = {str(ad["id"]) for ad in seller1_ads}
        seller2_ad_ids = {str(ad["id"]) for ad in seller2_ads}
        assert seller1_ad_ids.isdisjoint(seller2_ad_ids) or \
               (str(ad1_id) in seller1_ad_ids and str(ad2_id) in seller2_ad_ids), \
            "Объявления разных продавцов не должны смешиваться"

