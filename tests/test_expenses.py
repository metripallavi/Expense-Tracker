def test_create_expense_success(client):
    response = client.post(
        "/expenses",
        json={
            "amount": "100.50",
            "category": "Food",
            "description": "Lunch",
            "date": "2025-04-01",
        },
        headers={"Idempotency-Key": "test-key-1"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == "100.50"
    assert data["category"] == "Food"
    assert data["description"] == "Lunch"
    assert data["date"] == "2025-04-01"


def test_create_expense_is_idempotent(client):
    payload = {
        "amount": "250.00",
        "category": "Travel",
        "description": "Taxi",
        "date": "2025-04-02",
    }

    first = client.post(
        "/expenses",
        json=payload,
        headers={"Idempotency-Key": "same-key"},
    )
    second = client.post(
        "/expenses",
        json=payload,
        headers={"Idempotency-Key": "same-key"},
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] == second.json()["id"]

    list_response = client.get("/expenses")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_filter_expenses_by_category(client):
    client.post(
        "/expenses",
        json={
            "amount": "50.00",
            "category": "Food",
            "description": "Breakfast",
            "date": "2025-04-01",
        },
        headers={"Idempotency-Key": "food-1"},
    )
    client.post(
        "/expenses",
        json={
            "amount": "75.00",
            "category": "Travel",
            "description": "Bus",
            "date": "2025-04-02",
        },
        headers={"Idempotency-Key": "travel-1"},
    )

    response = client.get("/expenses?category=Food&sort=date_desc")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "Food"


def test_sort_expenses_newest_first(client):
    client.post(
        "/expenses",
        json={
            "amount": "30.00",
            "category": "Food",
            "description": "Old",
            "date": "2025-04-01",
        },
        headers={"Idempotency-Key": "sort-1"},
    )
    client.post(
        "/expenses",
        json={
            "amount": "40.00",
            "category": "Food",
            "description": "New",
            "date": "2025-04-10",
        },
        headers={"Idempotency-Key": "sort-2"},
    )

    response = client.get("/expenses?sort=date_desc")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["description"] == "New"
    assert data[1]["description"] == "Old"