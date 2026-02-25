def test_stats(client):
    response = client.get("/api/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total"] == 28
    assert stats["in_stock"] == 17
    assert stats["low_stock"] == 7
    assert stats["out_of_stock"] == 4


def test_stats_after_delete(client):
    # Delete an in-stock product
    products = client.get("/api/products", params={"status": "In Stock"}).json()
    client.delete(f"/api/products/{products[0]['id']}")

    stats = client.get("/api/stats").json()
    assert stats["total"] == 27
    assert stats["in_stock"] == 16


def test_stats_after_stock_change(client):
    # Change an in-stock product to out-of-stock
    products = client.get("/api/products", params={"status": "In Stock"}).json()
    product_id = products[0]["id"]
    client.patch(f"/api/products/{product_id}", json={"stock": 0})

    stats = client.get("/api/stats").json()
    assert stats["total"] == 28
    assert stats["in_stock"] == 16
    assert stats["out_of_stock"] == 5
