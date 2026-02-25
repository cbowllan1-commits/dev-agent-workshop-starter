def test_list_products(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 28


def test_get_product(client):
    products = client.get("/api/products").json()
    product_id = products[0]["id"]

    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id


def test_get_product_not_found(client):
    response = client.get("/api/products/nonexistent-id")
    assert response.status_code == 404


def test_create_product(client):
    new_product = {
        "name": "Test Widget",
        "category": "Electronics",
        "price": 29.99,
        "stock": 50,
        "sku": "TEST-001",
    }
    response = client.post("/api/products", json=new_product)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Widget"
    assert data["status"] == "In Stock"
    assert data["id"] is not None

    # Verify it was added
    products = client.get("/api/products").json()
    assert len(products) == 29


def test_create_product_validation_error(client):
    invalid_product = {
        "name": "",
        "category": "Electronics",
        "price": 29.99,
        "stock": 50,
        "sku": "TEST-001",
    }
    response = client.post("/api/products", json=invalid_product)
    assert response.status_code == 422


def test_create_product_invalid_category(client):
    invalid_product = {
        "name": "Test Widget",
        "category": "InvalidCategory",
        "price": 29.99,
        "stock": 50,
        "sku": "TEST-001",
    }
    response = client.post("/api/products", json=invalid_product)
    assert response.status_code == 422


def test_update_product(client):
    products = client.get("/api/products").json()
    product_id = products[0]["id"]

    response = client.patch(f"/api/products/{product_id}", json={"price": 999.99})
    assert response.status_code == 200
    assert response.json()["price"] == 999.99


def test_update_product_stock_changes_status(client):
    # Create a product with high stock (In Stock)
    new_product = {
        "name": "Status Test",
        "category": "Hardware",
        "price": 10.00,
        "stock": 50,
        "sku": "STAT-001",
    }
    created = client.post("/api/products", json=new_product).json()
    assert created["status"] == "In Stock"

    # Update to low stock
    updated = client.patch(f"/api/products/{created['id']}", json={"stock": 5}).json()
    assert updated["status"] == "Low Stock"

    # Update to out of stock
    updated = client.patch(f"/api/products/{created['id']}", json={"stock": 0}).json()
    assert updated["status"] == "Out of Stock"


def test_update_product_not_found(client):
    response = client.patch("/api/products/nonexistent-id", json={"price": 10.00})
    assert response.status_code == 404


def test_delete_product(client):
    products = client.get("/api/products").json()
    product_id = products[0]["id"]

    response = client.delete(f"/api/products/{product_id}")
    assert response.status_code == 204

    # Verify it was removed
    products = client.get("/api/products").json()
    assert len(products) == 27


def test_delete_product_not_found(client):
    response = client.delete("/api/products/nonexistent-id")
    assert response.status_code == 404
