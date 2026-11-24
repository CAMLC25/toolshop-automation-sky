"""BDD tests for Shopping Cart feature."""
import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage

pytestmark = [pytest.mark.bdd, pytest.mark.ui]

scenarios("cart.feature")


@given("I am on the home page", target_fixture="home")
def home(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    return home


@when(parsers.parse('I open the product "{product}"'), target_fixture="product_page")
def open_product(home, product):
    return home.open_product(product)


@when(parsers.parse("I add it to the cart with quantity {quantity:d}"), target_fixture="unit_price")
def add_to_cart(product_page, quantity):
    unit = product_page.price()
    product_page.add_to_cart(quantity=quantity)
    expect(product_page.cart_quantity).to_have_text(str(quantity))
    return unit


@when("I open the cart", target_fixture="cart")
def open_cart(product_page):
    return product_page.go_to_cart()


@then(parsers.parse('the cart contains "{product}"'))
def cart_contains(cart, product):
    expect(cart.product_titles).to_have_count(1)
    expect(cart.product_titles.first).to_have_text(product)


@then(parsers.parse("the line price equals the unit price times {quantity:d}"))
def line_price_equals(cart, unit_price, quantity):
    assert cart.line_totals()[0] == pytest.approx(unit_price * quantity)


@then("the cart total equals the sum of the line prices")
def total_equals_sum(cart):
    assert cart.total_value() == pytest.approx(sum(cart.line_totals()))
