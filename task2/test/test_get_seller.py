import random
import time
import requests
from conftest import BASE_URL


# ------------------------
# TC-400
# ------------------------
def test_get_single_item_by_seller(create_item):
    seller_id = 123456
    item_id = create_item(seller_id)

    resp = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert any(item["id"] == item_id for item in data)

    item = data[0]
    assert "id" in item
    assert "sellerId" in item
    assert "name" in item
    assert "price" in item
    assert "statistics" in item
    assert "createdAt" in item


# ------------------------
# TC-401
# ------------------------
def test_get_multiple_items_by_seller(create_item):
    seller_id = 123457

    ids = [create_item(seller_id) for _ in range(3)]

    resp = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) >= 3

    for item in data:
        assert item["sellerId"] == seller_id


# ------------------------
# TC-402
# ------------------------
def test_get_empty_items_by_seller():
    seller_id = random.randint(900000, 999999)

    resp = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
    assert resp.status_code == 200

    data = resp.json()
    assert data == []


# ------------------------
# TC-403
# ------------------------
def test_get_items_seller_zero():
    """Проверяем поведение GET для sellerId=0 — должен вернуть 200 OK с пустым списком"""
    get_resp = requests.get(f"{BASE_URL}/api/1/0/item")

    assert (
        get_resp.status_code == 200
    ), f"Ожидался 200, но получили {get_resp.status_code}"

    data = get_resp.json()
    assert isinstance(data, list), f"Ожидался список, но получили: {type(data)}"
    assert len(data) == 0, f"Ожидался пустой список, но получили: {data}"


# ------------------------
# TC-404 (идемпотентность)
# ------------------------
def test_get_items_idempotent(create_item):
    seller_id = 123458
    create_item(seller_id)

    resp1 = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
    resp2 = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")

    assert resp1.status_code == 200
    assert resp2.status_code == 200
    assert resp1.json() == resp2.json()


# ------------------------
# TC-405 (порядок)
# ------------------------
def test_get_items_order(create_item):
    seller_id = 123459

    create_item(seller_id)
    time.sleep(1)
    create_item(seller_id)
    time.sleep(1)
    create_item(seller_id)

    resp = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
    assert resp.status_code == 200

    data = resp.json()

    # Просто фиксируем порядок
    ids = [item["id"] for item in data]
    print("Порядок id:", ids)

    assert len(ids) >= 3


# ------------------------
# TC-406 (удаление)
# ------------------------
def test_get_items_after_delete(create_item):
    seller_id = 123460

    item1 = create_item(seller_id)
    item2 = create_item(seller_id)

    # Пытаемся удалить (но API может не поддерживать)
    del_resp = requests.delete(f"{BASE_URL}/api/1/item/{item1}")

    if del_resp.status_code in [200, 204]:
        resp = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
        data = resp.json()

        ids = [item["id"] for item in data]
        assert item1 not in ids
        assert item2 in ids
    else:
        # фиксируем поведение API
        assert del_resp.status_code == 405


# ------------------------
# TC-407
# ------------------------
def test_get_items_null():
    resp = requests.get(f"{BASE_URL}/api/1/null/item")
    assert resp.status_code in [400, 404]


# ------------------------
# TC-409
# ------------------------
def test_get_items_no_accept_header(create_item):
    seller_id = 123461
    create_item(seller_id)

    resp = requests.get(f"{BASE_URL}/api/1/{seller_id}/item", headers={})  # без Accept

    assert resp.status_code == 200
