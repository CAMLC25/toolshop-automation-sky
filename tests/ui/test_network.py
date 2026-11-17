"""Network routing and mocking tests."""
import json
import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage

# Open DevTools > Network on the home page and look at how the product list is loaded:
#   PROD:   QUERY https://api.practicesoftwaretesting.com/products          (JSON body)
#   BUGGY:  GET   https://api-with-bugs.../products?between=price,1&page=1
# One regex catches both, and NOT /products/search or /products/{id}:
PRODUCT_LIST = re.compile(r"/products(\?.*)?$")
EMPTY_PAGE = {
    "current_page": 1,
    "data": [],
    "from": None,
    "last_page": 1,
    "per_page": 9,
    "to": None,
    "total": 0,
}


# ---------------------------------------------------------------- B2.7
@pytest.mark.ui
def test_home_without_images_still_lists_products(page):
    """Goal: the page works properly without images.
    Precondition: none.
    Expected: product names visible and at least one image request was aborted."""
    blocked = []

    def block_images(route):
        blocked.append(route.request.url)
        route.abort()

    page.route(re.compile(r"\.(png|jpe?g|webp|avif|svg)(\?.*)?$"), block_images)
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    assert blocked


# ---------------------------------------------------------------- B2.8
@pytest.mark.ui
def test_home_with_empty_product_list_shows_no_results(page):
    """Goal: empty state of the product grid.
    Precondition: list API mocked with EMPTY_PAGE.
    Expected: 'There are no products found.' message and 0 product cards."""
    page.route(
        PRODUCT_LIST,
        lambda route: route.fulfill(
            status=200, content_type="application/json", body=json.dumps(EMPTY_PAGE)
        ),
    )
    home = HomePage(page).open()
    expect(home.no_results).to_have_text("There are no products found.")
    expect(home.product_names).to_have_count(0)
