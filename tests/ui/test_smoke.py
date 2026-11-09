"""Sprint 1 - 4 smoke tests for Toolshop.

Run: pytest -m smoke
"""
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.contact_page import ContactPage


# ---------------------------------------------------------------- Test 1
@pytest.mark.smoke
def test_search_keyword_shows_matching_products(page):
    """Goal: search filters the grid.
    Precondition: none.
    Expected: caption shows the keyword and every product name contains it."""
    home = HomePage(page).open().search("pliers")
    expect(home.search_completed).to_be_visible()
    expect(home.search_caption).to_contain_text("pliers")
    names = home.product_names.all_inner_texts()
    assert names, "search returned no products"
    assert all("pliers" in n.lower() for n in names), names


# ---------------------------------------------------------------- Test 2
@pytest.mark.smoke
def test_product_add_quantity_three_updates_cart_badge(page):
    """Goal: add-to-cart uses the chosen quantity.
    Precondition: product 'Claw Hammer' exists.
    Expected: toast 'Product added to shopping cart' and the cart badge shows 3."""
    product = (
        HomePage(page)
        .open()
        .open_product("Claw Hammer")
        .add_to_cart(quantity=3)
    )
    expect(product.toast).to_contain_text("Product added to shopping cart")
    expect(product.cart_quantity).to_have_text("3")


# ---------------------------------------------------------------- Test 3
@pytest.mark.smoke
def test_login_wrong_password_shows_error(page):
    """Goal: invalid credentials are rejected.
    Precondition: an e-mail with no account.
    Expected: 'Invalid email or password' and the URL still ends with /auth/login."""
    login = LoginPage(page).open().login("nobody-here@example.com", "Wrong-Password-123")
    expect(login.error).to_contain_text("Invalid email or password")
    assert page.url.endswith("/auth/login")


# ---------------------------------------------------------------- Test 4
@pytest.mark.smoke
def test_contact_empty_form_shows_required_errors(page):
    """Goal: contact form validation for empty submission.
    Precondition: none.
    Expected: 'Subject is required' and 'Message is required' errors are visible."""
    contact = ContactPage(page).open().submit()
    expect(contact.errors.filter(has_text="Subject is required")).to_be_visible()
    expect(contact.errors.filter(has_text="Message is required")).to_be_visible()
