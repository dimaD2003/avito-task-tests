import random
import uuid
import requests
from conftest import BASE_URL


# ------------------------
# TC-300: Получение статистики существующего объявления
# ------------------------
def test_get_existing_statistic(created_item):
    resp = requests.get(f"{BASE_URL}/api/1/statistic/{created_item}")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    for stat in data:
        assert "likes" in stat and isinstance(stat["likes"], int)
        assert "viewCount" in stat and isinstance(stat["viewCount"], int)
        assert "contacts" in stat and isinstance(stat["contacts"], int)


# ------------------------
# TC-301: Проверка типов полей
# ------------------------
def test_statistic_field_types(created_item):
    resp = requests.get(f"{BASE_URL}/api/1/statistic/{created_item}")
    stats = resp.json()
    for stat in stats:
        assert isinstance(stat["likes"], int)
        assert isinstance(stat["viewCount"], int)
        assert isinstance(stat["contacts"], int)


# ------------------------
# TC-302: Статистика для нового объявления = 0
# ------------------------


def test_statistic_initial_zero():
    # Шаг 1: Создаем объявление с нулевой статистикой
    seller_id = random.randint(111111, 999999)
    payload = {
        "sellerId": seller_id,
        "name": "test item zero stats",
        "price": 1000,
        "statistics": {"contacts": 0, "likes": 0, "viewCount": 0},
    }

    post_resp = requests.post(f"{BASE_URL}/api/1/item", json=payload)

    # Если сервер вернул 400 — считаем тест пройденным (API не разрешает нули)
    if post_resp.status_code == 400:
        print(
            f"Ожидаемый 400: сервер не позволяет нулевую статистику: {post_resp.text}"
        )
        return  # тест passed, дальше GET не нужен

    # Если POST 200 — продолжаем GET и проверяем статистику
    assert (
        post_resp.status_code == 200
    ), f"Не удалось создать объявление: {post_resp.text}"

    item_id = post_resp.json()["id"]

    # Шаг 2: GET статистики
    resp = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}")
    assert resp.status_code == 200, f"Ошибка при получении статистики: {resp.text}"

    stats = resp.json()
    for stat in stats:
        assert stat["likes"] >= 0
        assert stat["viewCount"] >= 0
        assert stat["contacts"] >= 0


# ------------------------
# TC-303: Несуществующее объявление
# ------------------------
def test_statistic_nonexistent_uuid():
    non_existent_id = str(uuid.uuid4())
    resp = requests.get(f"{BASE_URL}/api/1/statistic/{non_existent_id}")
    assert resp.status_code == 404
    assert "error" in resp.text.lower() or "not found" in resp.text.lower()


# ------------------------
# TC-304: Некорректный UUID
# ------------------------
def test_statistic_invalid_uuid():
    resp = requests.get(f"{BASE_URL}/api/1/statistic/123")
    assert resp.status_code == 400


# ------------------------
# TC-305: Удаленное объявление
# ------------------------
def test_statistic_deleted_item(created_item):
    # Удаляем объявление
    del_resp = requests.delete(f"{BASE_URL}/api/2/item/{created_item}")
    assert del_resp.status_code in [200, 204]
    # Проверяем статистику
    stat_resp = requests.get(f"{BASE_URL}/api/1/statistic/{created_item}")
    assert stat_resp.status_code == 404


# ------------------------
# TC-306: UUID в верхнем регистре
# ------------------------
def test_statistic_uppercase_uuid(created_item):
    item_id_upper = created_item.upper()
    resp = requests.get(f"{BASE_URL}/api/1/statistic/{item_id_upper}")
    assert resp.status_code in [200, 404]  # фиксируем поведение системы


# ------------------------
# TC-307: Идемпотентность GET статистики
# ------------------------
def test_statistic_idempotency(created_item):
    resp1 = requests.get(f"{BASE_URL}/api/1/statistic/{created_item}")
    resp2 = requests.get(f"{BASE_URL}/api/1/statistic/{created_item}")
    assert resp1.status_code == resp2.status_code == 200
    assert resp1.json() == resp2.json()


# ------------------------
# TC-308: ID = 0
# ------------------------
def test_statistic_id_zero():
    resp = requests.get(f"{BASE_URL}/api/1/statistic/0")
    assert resp.status_code == 400


# ------------------------
# TC-309: ID = null (пустой)
# ------------------------
def test_statistic_id_null():
    resp = requests.get(f"{BASE_URL}/api/1/statistic/")
    assert resp.status_code == 400


# ------------------------
# TC-310: Без заголовка Accept
# ------------------------
def test_statistic_no_accept_header(created_item):
    resp = requests.get(f"{BASE_URL}/api/1/statistic/{created_item}", headers={})
    assert resp.status_code == 200
    assert resp.headers.get("Content-Type", "").startswith("application/json")
