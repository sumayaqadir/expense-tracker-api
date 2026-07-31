from fastapi.testclient import TestClient
from main import app, expenses

client = TestClient(app)


def setup_function():
    """Reset in-memory data before each test so tests don't affect each other."""
    expenses.clear()


def test_add_expense():
    response = client.post("/expenses", json={
        "title": "Coffee",
        "amount": 4.5,
        "category": "Food",
        "date": "2026-07-31"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Coffee"
    assert "id" in data


def test_get_all_expenses():
    client.post("/expenses", json={
        "title": "Coffee", "amount": 4.5, "category": "Food", "date": "2026-07-31"
    })
    response = client.get("/expenses")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_by_category():
    client.post("/expenses", json={
        "title": "Coffee", "amount": 4.5, "category": "Food", "date": "2026-07-31"
    })
    client.post("/expenses", json={
        "title": "Bus", "amount": 2.0, "category": "Transport", "date": "2026-07-31"
    })
    response = client.get("/expenses/category/Food")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["category"] == "Food"


def test_totals():
    client.post("/expenses", json={
        "title": "Coffee", "amount": 4.5, "category": "Food", "date": "2026-07-31"
    })
    client.post("/expenses", json={
        "title": "Bus", "amount": 2.0, "category": "Transport", "date": "2026-07-31"
    })
    response = client.get("/expenses/total")
    assert response.status_code == 200
    data = response.json()
    assert data["overall_total"] == 6.5
    assert data["by_category"]["Food"] == 4.5
    assert data["by_category"]["Transport"] == 2.0


def test_delete_expense():
    add_response = client.post("/expenses", json={
        "title": "Coffee", "amount": 4.5, "category": "Food", "date": "2026-07-31"
    })
    expense_id = add_response.json()["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Expense deleted"

    # confirm it's actually gone
    get_response = client.get("/expenses")
    assert len(get_response.json()) == 0


def test_delete_nonexistent_expense_returns_404():
    response = client.delete("/expenses/does-not-exist")
    assert response.status_code == 404
