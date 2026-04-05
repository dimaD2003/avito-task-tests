import random
import requests
from conftest import BASE_URL


# ===========================
# TC-100: Получение объявления по валидному id
# ===========================
def test_get_item_valid_id(created_item):
    item_id = created_item
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == item_id


# ===========================
# TC-101: Проверка структуры и типа полей ответа
# ===========================
def test_get_item_field_types(created_item):
    item_id = created_item
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    data = response.json()[0]

    assert isinstance(data["id"], str)
    assert isinstance(data["sellerId"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["price"], int)
    assert isinstance(data["statistics"], dict)
    assert isinstance(data["statistics"]["likes"], int)
    assert isinstance(data["statistics"]["viewCount"], int)
    assert isinstance(data["statistics"]["contacts"], int)
    assert isinstance(data["createdAt"], str)


# ===========================
# TC-102: Проверка количества элементов
# ===========================
def test_get_item_array_length(created_item):
    item_id = created_item
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    data = response.json()
    assert len(data) == 1


# ===========================
# TC-103: Несуществующий id
# ===========================
def test_get_item_not_exists():
    item_id = "11111111-1111-1111-1111-111111111111"
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert response.status_code in [400, 404]
    json_data = response.json()
    assert "status" in json_data
    assert "result" in json_data


# ===========================
# TC-104: Невалидный id (строка)
# ===========================
def test_get_item_invalid_id_string():
    item_id = "abc"
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert response.status_code == 400


# ===========================
# TC-105: Пустой id
# ===========================
def test_get_item_empty_id():
    response = requests.get(f"{BASE_URL}/api/1/item/")
    assert response.status_code == 400


# ===========================
# TC-106: Проверка идемпотентности
# ===========================
def test_get_item_idempotency(created_item):
    item_id = created_item
    results = []
    for _ in range(3):
        response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
        assert response.status_code == 200
        results.append(response.json())
    assert results[0] == results[1] == results[2]


# ===========================
# TC-107: SQL-инъекция в id
# ===========================
def test_get_item_sql_injection():
    item_id = "baf35c71-3e07-4bc4-8acf-083a49bb5f5f OR 1=1"
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert response.status_code in [400, 404]


# ===========================
# TC-108: XSS-инъекция
# ===========================
def test_get_item_xss_injection():
    item_id = "<script>alert(1)</script>"
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert response.status_code in [400, 404]


# ===========================
# TC-109: UUID короче 36 символов
# ===========================
def test_get_item_short_uuid():
    item_id = "baf35c71-3e07"
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert response.status_code == 400


# ===========================
# TC-110: Получение удаленного объявления
# ===========================
def test_get_item_deleted():
    # Создать и удалить объявление
    seller_id = random.randint(111111, 999999)
    payload = {
        "sellerId": seller_id,
        "name": "to_delete",
        "price": 1000,
        "statistics": {"contacts": 10, "likes": 5, "viewCount": 20},
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    item_id = response.json()["status"].split()[-1]

    requests.delete(f"{BASE_URL}/api/2/item/{item_id}")
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert response.status_code == 404


# ===========================
# TC-111: Проверка заголовка Accept
# ===========================
def test_get_item_accept_header(created_item):
    item_id = created_item

    response = requests.get(
        f"{BASE_URL}/api/1/item/{item_id}", headers={"Accept": "text/plain"}
    )
    assert response.status_code in [200, 406]

    response = requests.get(
        f"{BASE_URL}/api/1/item/{item_id}", headers={"Accept": "application/xml"}
    )
    assert response.status_code in [200, 406]


# ===========================
# TC-112: Передача UUID в верхнем регистре
# ===========================
def test_get_item_uppercase_uuid(created_item):
    item_id = created_item
    item_id_upper = item_id.upper()

    response = requests.get(f"{BASE_URL}/api/1/item/{item_id_upper}")
    assert response.status_code in [200, 404]
