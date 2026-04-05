import random
import re

import pytest
import requests

BASE_URL = "https://qa-internship.avito.com"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def random_seller_id():
    return random.randint(111111, 999999)


# автогенерация нового id объявления
@pytest.fixture
def created_item():
    seller_id = random.randint(111111, 999999)

    payload = {
        "sellerId": seller_id,
        "name": "test item",
        "price": 1000,
        "statistics": {"contacts": 501, "likes": 150, "viewCount": 220},
    }

    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)

    assert (
        response.status_code == 200
    ), f"Не удалось создать объявление: {response.text}"

    # вытащим UUID из строки
    match = re.search(r"([a-f0-9\-]{36})", response.json()["status"])
    assert match, f"UUID не найден в ответе: {response.json()['status']}"

    item_id = match.group(1)
    return item_id


# автогенерация нового объекта объявления
@pytest.fixture
def create_item():
    def _create(seller_id):
        payload = {
            "sellerId": seller_id,
            "name": "test item2",
            "price": 1000,
            "statistics": {"contacts": 121, "likes": 1313, "viewCount": 122},
        }

        response = requests.post(f"{BASE_URL}/api/1/item", json=payload)

        # проверка ответа
        assert response.status_code == 200, f"Ошибка создания: {response.text}"

        data = response.json()

        # извлекаем UUID из строки status
        match = re.search(r"([a-f0-9\-]{36})", data.get("status", ""))
        assert match, f"UUID не найден в ответе: {data}"

        item_id = match.group(1)

        return item_id

    return _create
