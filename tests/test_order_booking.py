from pages.home_page import HomePage
from pages.order_page import OrderPage
from data.home_page_data import HomePageData
import pytest

@pytest.mark.smoke
def test_home_page_display(browser_setup):
    home_page = HomePage(browser_setup)
    home_page.navigate_to_home_page()
    home_page.home_menu_display()
    home_page.sign_out_display()

@pytest.mark.smoke
def test_get_product_details(browser_setup, shared_data):
    home_page = HomePage(browser_setup)
    home_page.get_all_product_api(shared_data)

@pytest.mark.regression
@pytest.mark.dependency(depends=["test_get_product_details"])
@pytest.mark.parametrize("product", [HomePageData.adidas_product])
def test_add_to_cart(browser_setup, shared_data, product):
    home_page = HomePage(browser_setup)
    home_page.add_product_to_cart(shared_data, product)

@pytest.mark.regression
@pytest.mark.dependency(depends=["test_add_to_cart"])
def test_create_order(browser_setup, shared_data):
    order_page = OrderPage(browser_setup)
    order_page.create_order(shared_data)

@pytest.mark.regression
@pytest.mark.dependency(depends=["test_create_order"])
@pytest.mark.parametrize("product", [HomePageData.adidas_product])
def test_verify_order(browser_setup, shared_data, product):
    order_page = OrderPage(browser_setup)
    order_page.navigate_to_order_page()
    order_page.verify_order_id(shared_data)
    order_page.verify_product_name()
    order_page.verify_product_price(shared_data, product)

@pytest.mark.regression
@pytest.mark.dependency(depends=["test_verify_order"])
def test_delete_order(browser_setup):
    order_page = OrderPage(browser_setup)
    order_page.click_delete_btn()
    order_page.verify_no_orders_msg()

