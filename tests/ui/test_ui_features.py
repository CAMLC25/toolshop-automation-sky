"""UI tests covering functional areas for Sprint 2 (Bổ sung 8 test để đủ 12 test UI)."""
import re

import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


# ================================================================
# NHÓM 1: DANH SÁCH & TÌM KIẾM (Test 2/2 - Test 1 đã có trong test_smoke.py)
# ================================================================
@pytest.mark.ui
def test_search_unknown_keyword_shows_no_results_message(page):
    """Goal: verify empty search state displays proper message and no products.
    Precondition: none.
    Expected: message 'There are no products found.' and 0 product cards displayed."""
    home = HomePage(page).open().search("zzz-no-such-tool")
    expect(home.no_results).to_have_text("There are no products found.")
    expect(home.product_names).to_have_count(0)


# ================================================================
# NHÓM 2: BỘ LỌC (FILTER & SORT) (Test 1/2 & 2/2)
# ================================================================
@pytest.mark.ui
def test_sort_by_price_ascending_sorts_products(page):
    """Goal: sort products by price ascending.
    Precondition: none.
    Expected: prices on the first page are sorted in ascending order."""
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    home.sort_by("price,asc")
    expect(home.sorting_completed).to_be_visible()
    prices = home.prices()
    assert prices == sorted(prices), prices


@pytest.mark.ui
def test_filter_by_category_checkbox_filters_products(page):
    """Goal: category checkbox filter restricts product list.
    Precondition: none.
    Expected: all displayed product names belong to the selected category."""
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    home.filter_by_category("Hammer")
    expect(home.product_names.first).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names, "No products displayed for selected category"
    assert all("hammer" in n.lower() for n in names), names


# ================================================================
# NHÓM 3: CHI TIẾT SẢN PHẨM (Test 1/2 - Test 2 đã có trong test_smoke.py)
# ================================================================
@pytest.mark.ui
def test_product_detail_shows_correct_name_and_price(page):
    """Goal: product details page shows accurate name and positive price.
    Precondition: product 'Claw Hammer' exists.
    Expected: product page displays 'Claw Hammer' and unit price > 0."""
    product = HomePage(page).open().open_product("Claw Hammer")
    expect(product.name).to_have_text("Claw Hammer")
    assert product.price() > 0


# ================================================================
# NHÓM 4: GIỎ HÀNG (CART) (Test 1/2 & 2/2)
# ================================================================
@pytest.mark.ui
def test_cart_line_price_equals_unit_price_times_quantity(page):
    """Goal: verify cart line price arithmetic (unit price x quantity).
    Precondition: a fresh browser context.
    Expected: line total equals unit price multiplied by 2 and total matches sum."""
    product = HomePage(page).open().open_product("Combination Pliers")
    unit = product.price()
    product.add_to_cart(quantity=2)
    expect(product.cart_quantity).to_have_text("2")
    cart = product.go_to_cart()
    expect(cart.product_titles).to_have_count(1)
    assert cart.line_totals() == [pytest.approx(unit * 2)]
    assert cart.total_value() == pytest.approx(sum(cart.line_totals()))


@pytest.mark.ui
def test_cart_continue_shopping_returns_to_home(page):
    """Goal: continue shopping button navigates back to home page.
    Precondition: product added to cart.
    Expected: clicking continue shopping returns to home and shows product grid."""
    cart = HomePage(page).open().open_product("Hammer").add_to_cart().go_to_cart()
    expect(cart.product_titles.first).to_have_text("Hammer")
    cart.continue_shopping.click()
    expect(HomePage(page).product_names.first).to_be_visible()


# ================================================================
# NHÓM 5: XÁC THỰC (AUTH) (Test 2/2 - Test 1 đã có trong test_smoke.py)
# ================================================================
@pytest.mark.ui
def test_login_empty_form_shows_required_errors(page):
    """Goal: client-side validation on empty login form submission.
    Precondition: none.
    Expected: required errors for both email and password fields."""
    login = LoginPage(page).open()
    login.submit_button.click()
    expect(login.email_error).to_contain_text("Email is required")
    expect(login.password_error).to_contain_text("Password is required")


# ================================================================
# NHÓM 6: LIÊN HỆ & TÀI KHOẢN (Test 2/2 - Test 1 đã có trong test_smoke.py)
# ================================================================
@pytest.mark.ui
def test_account_page_logged_in_shows_user_menu(logged_in_page):
    """Goal: verify reuse of saved login state via storage_state fixture.
    Precondition: user authenticated via logged_in_page fixture.
    Expected: account page title is 'My account' and user menu displays user name."""
    account = AccountPage(logged_in_page).open()
    expect(account.title).to_have_text("My account")
    expect(account.nav_menu).to_contain_text("QA Bot")
