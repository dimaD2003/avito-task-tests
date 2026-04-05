import requests
from conftest import BASE_URL  # твой config/conftest файл


# -----------------------------
# TC-200 - Сохранение объявления с валидным Request body
# -----------------------------
def test_post_item_valid_body():
    payload = {
        "sellerId": 123456,
        "name": "Ноутбук",
        "price": 50000,
        "statistics": {"likes": 10, "viewCount": 100, "contacts": 5},
    }

    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 200
    assert "status" in response.json()
    item_id = response.json()["status"].split()[-1]
    assert len(item_id) == 36  # проверяем что id похож на UUID


# -----------------------------
# TC-201 - Создание без обязательных полей
# -----------------------------
def test_post_item_missing_required_fields():
    payload = {
        "sellerId": None,
        "name": None,
        "price": None,
        "statistics": {"likes": None, "viewCount": None, "contacts": None},
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 400


# -----------------------------
# TC-202 - SellerID слишком большое число
# -----------------------------
def test_post_item_sellerid_too_large():
    payload = {
        "sellerId": 99999999999999999999,
        "name": "Ноутбук",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 400


# -----------------------------
# TC-203 - Идемпотентность
# -----------------------------
def test_post_item_idempotency():
    payload = {
        "sellerId": 123456,
        "name": "Ноутбук",
        "price": 5000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }
    response1 = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    response2 = requests.post(f"{BASE_URL}/api/1/item", json=payload)

    assert response1.status_code == 200
    assert response2.status_code == 200
    id1 = response1.json()["status"].split()[-1]
    id2 = response2.json()["status"].split()[-1]
    assert id1 != id2  # два разных объявления


# -----------------------------
# TC-204 - Отрицательные значения statistics
# -----------------------------
def test_post_item_negative_statistics():
    payload = {
        "sellerId": 123456,
        "name": "Ноутбук",
        "price": 5000,
        "statistics": {"likes": -12, "viewCount": -1, "contacts": -5},
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    # поведение зависит от сервера: либо OK, либо 400
    assert response.status_code in [200, 400]


# -----------------------------
# TC-205 - SellerID в виде строки
# -----------------------------
def test_post_item_sellerid_string():
    payload = {
        "sellerId": "123456",
        "name": "Ноутбук",
        "price": 5000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 400


# -----------------------------
# TC-206 - Цена = 0
# -----------------------------
def test_post_item_price_zero():
    payload = {
        "sellerId": 123456,
        "name": "Ноутбук",
        "price": 0,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 400


# -----------------------------
# TC-207 - Пустое название
# -----------------------------
def test_post_item_empty_name():
    payload = {
        "sellerId": 123456,
        "name": "",
        "price": 5000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 400


# -----------------------------
# TC-208 - Без Content-Type
# -----------------------------
def test_post_item_no_content_type():
    payload = '{"sellerId":123456,"name":"Ноутбук","price":5000,"statistics":{"likes":1,"viewCount":1,"contacts":1}}'
    response = requests.post(
        f"{BASE_URL}/api/1/item", data=payload
    )  # без json=, нет заголовка
    assert response.status_code in [200, 400]


# -----------------------------
# TC-209 - Content-Type: text/plain
# -----------------------------
def test_post_item_text_plain():
    payload = '{"sellerId":123456,"name":"Ноутбук","price":5000,"statistics":{"likes":1,"viewCount":1,"contacts":1}}'
    headers = {"Content-Type": "text/plain"}
    response = requests.post(f"{BASE_URL}/api/1/item", data=payload, headers=headers)
    assert response.status_code in [200, 400, 415]


# -----------------------------
# TC-210 - Лишние поля
# -----------------------------
def test_post_item_extra_fields():
    payload = {
        "sellerId": 123456,
        "name": "Ноутбук",
        "price": 5000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
        "extraField": "extra",
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 200


# -----------------------------
# TC-212 - Невалидный JSON
# -----------------------------
def test_post_item_invalid_json():
    payload = '{"sellerId":123,"name":"frf","price":-10,"statistics":{"likes":12,"viewCount":12,"contacts":12,}}'  # лишняя запятая
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/api/1/item", data=payload, headers=headers)
    assert response.status_code == 400
