import pytest
import requests


class TestGetAdStats:

    def test_get_stats_existing_ad(self, session, base_url, created_ad):
        ad_id = created_ad["id"]
        response = session.get(f"{base_url}/api/1/statistic/{ad_id}")
        
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        
        data = response.json()
        assert isinstance(data, (list, dict)), "Ответ должен быть массивом или объектом"
        if isinstance(data, list):
            assert len(data) > 0, "Массив статистики не должен быть пустым"
            if len(data) > 0:
                stat = data[0]
                assert "likes" in stat or "viewCount" in stat or "contacts" in stat, \
                    "Статистика должна содержать хотя бы одно поле (likes, viewCount, contacts)"
        else:
            assert len(data) > 0, "Статистика должна содержать данные"

    def test_get_stats_nonexistent_ad(self, session, base_url):
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        response = session.get(f"{base_url}/api/1/statistic/{nonexistent_id}")
        
        assert response.status_code in [400, 404], \
            f"Ожидался статус 400 или 404, получен {response.status_code}. Ответ: {response.text}"

    def test_get_stats_invalid_id_format(self, session, base_url):
        invalid_id = "abc"
        response = session.get(f"{base_url}/api/1/statistic/{invalid_id}")
        
        assert response.status_code in [400, 404], \
            f"Ожидался статус 400 или 404, получен {response.status_code}. Ответ: {response.text}"

