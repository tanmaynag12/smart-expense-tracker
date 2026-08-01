import pytest
from fastapi.testclient import TestClient
from src import storage
from src.main import app

client = TestClient(app)


@pytest.fixture
def isolated_storage(tmp_path, monkeypatch):
    fake_file = tmp_path / "expenses.json"
    monkeypatch.setattr(storage, "DATA_FILE", fake_file)


def test_load_returns_empty_list_when_file_missing(isolated_storage):
    assert storage.load() == []


def test_save_then_load_round_trip(isolated_storage):
    data = [
        {
            "id": 1,
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        }
    ]
    storage.save(data)
    assert storage.load() == data


def test_add_expense_assigns_sequential_ids(isolated_storage):
    e1 = storage.add_expense(
        {
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        }
    )
    e2 = storage.add_expense(
        {
            "title": "Bus",
            "amount": 2.0,
            "category": "transport",
            "date": "2026-07-31",
        }
    )

    assert e1["id"] == 1
    assert e2["id"] == 2


def test_delete_expense_returns_false_for_unknown_id(isolated_storage):
    assert storage.delete_expense(999) is False


def test_delete_expense_returns_true_for_known_id(isolated_storage):
    e1 = storage.add_expense(
        {
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        }
    )

    assert storage.delete_expense(e1["id"]) is True


def test_create_expense_returns_201(isolated_storage):
    response = client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Coffee"
    assert body["id"] == 1


def test_create_expense_rejects_negative_amount(isolated_storage):
    response = client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": -5,
            "category": "food",
            "date": "2026-07-31",
        },
    )

    assert response.status_code == 422


def test_create_expense_rejects_blank_title(isolated_storage):
    response = client.post(
        "/expenses",
        json={
            "title": "   ",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )

    assert response.status_code == 422


def test_create_expense_rejects_invalid_date(isolated_storage):
    response = client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "not-a-date",
        },
    )

    assert response.status_code == 422


def test_list_expenses_empty(isolated_storage):
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json() == []


def test_list_expenses_returns_all(isolated_storage):
    client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )
    client.post(
        "/expenses",
        json={
            "title": "Bus",
            "amount": 2.0,
            "category": "transport",
            "date": "2026-07-31",
        },
    )

    response = client.get("/expenses")
    body = response.json()

    assert len(body) == 2
    assert body[0]["title"] == "Coffee"
    assert body[1]["title"] == "Bus"


def test_filter_by_category(isolated_storage):
    client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )
    client.post(
        "/expenses",
        json={
            "title": "Bus",
            "amount": 2.0,
            "category": "transport",
            "date": "2026-07-31",
        },
    )

    response = client.get("/expenses?category=food")
    body = response.json()

    assert len(body) == 1
    assert body[0]["title"] == "Coffee"


def test_filter_by_category_case_insensitive(isolated_storage):
    client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )

    response = client.get("/expenses?category=Food")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_by_category_no_matches(isolated_storage):
    client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )

    response = client.get("/expenses?category=entertainment")

    assert response.status_code == 200
    assert response.json() == []


def test_totals_empty(isolated_storage):
    response = client.get("/expenses/total")
    body = response.json()

    assert body["overall_total"] == 0
    assert body["by_category"] == {}


def test_totals_with_expenses(isolated_storage):
    client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )
    client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 10.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )
    client.post(
        "/expenses",
        json={
            "title": "Bus",
            "amount": 2.0,
            "category": "transport",
            "date": "2026-07-31",
        },
    )

    response = client.get("/expenses/total")
    body = response.json()

    assert body["overall_total"] == 17.0
    assert body["by_category"]["food"] == 15.0
    assert body["by_category"]["transport"] == 2.0


def test_delete_existing_expense(isolated_storage):
    create_response = client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )

    expense_id = create_response.json()["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")

    assert delete_response.status_code == 204

    list_response = client.get("/expenses")
    assert list_response.json() == []


def test_delete_nonexistent_expense(isolated_storage):
    response = client.delete("/expenses/999")

    assert response.status_code == 404


def test_delete_twice_returns_404_second_time(isolated_storage):
    create_response = client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 4.5,
            "category": "food",
            "date": "2026-07-31",
        },
    )

    expense_id = create_response.json()["id"]

    client.delete(f"/expenses/{expense_id}")

    second_delete = client.delete(f"/expenses/{expense_id}")

    assert second_delete.status_code == 404