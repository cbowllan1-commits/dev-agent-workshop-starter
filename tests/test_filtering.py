def test_filter_by_category(client):
    response = client.get("/api/products?category=Electronics")
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 8
    assert all(p["category"] == "Electronics" for p in products)


def test_filter_by_status_in_stock(client):
    response = client.get("/api/products", params={"status": "In Stock"})
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 17
    assert all(p["status"] == "In Stock" for p in products)


def test_filter_by_status_low_stock(client):
    response = client.get("/api/products", params={"status": "Low Stock"})
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 7
    assert all(p["status"] == "Low Stock" for p in products)


def test_filter_by_status_out_of_stock(client):
    response = client.get("/api/products", params={"status": "Out of Stock"})
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 4
    assert all(p["status"] == "Out of Stock" for p in products)


def test_search_by_name(client):
    response = client.get("/api/products?search=keyboard")
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 1
    assert products[0]["name"] == "Mechanical Keyboard"


def test_search_case_insensitive(client):
    response = client.get("/api/products?search=MONITOR")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 1
    assert any("Monitor" in p["name"] for p in products)


def test_combined_filters(client):
    response = client.get("/api/products", params={"category": "Electronics", "status": "In Stock"})
    assert response.status_code == 200
    products = response.json()
    assert all(p["category"] == "Electronics" for p in products)
    assert all(p["status"] == "In Stock" for p in products)
    assert len(products) == 5


def test_search_no_results(client):
    response = client.get("/api/products?search=nonexistentproduct")
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 0


def test_products_sorted_by_name(client):
    response = client.get("/api/products")
    products = response.json()
    names = [p["name"] for p in products]
    assert names == sorted(names)
