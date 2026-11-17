"""Cart API tests."""
import pytest


# ---------------------------------------------------------------- B2.6
@pytest.fixture
def new_cart(api):
    response = api.post("/carts")
    assert response.status == 201, response.text()
    return response.json()["id"]


@pytest.mark.api
def test_cart_add_product_quantity_two_is_stored(api, new_cart):
    """Goal: cart API stores the added product and quantity.
    Precondition: a new cart fixture and first available product.
    Expected: cart contains exactly 1 item with quantity 2 and matching product id."""
    prod_res = api.get("/products", params={"page": 1})
    assert prod_res.status == 200, prod_res.text()
    product = prod_res.json()["data"][0]

    added = api.post(f"/carts/{new_cart}", data={"product_id": product["id"], "quantity": 2})
    assert added.status == 200, added.text()

    cart_res = api.get(f"/carts/{new_cart}")
    assert cart_res.status == 200, cart_res.text()
    items = cart_res.json()["cart_items"]
    assert len(items) == 1
    assert items[0]["quantity"] == 2
    assert str(items[0]["product_id"]) == str(product["id"])
