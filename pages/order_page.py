from locators.home_page_locators import HomePageLocators
from locators.order_page_locators import OrderPageLocators
from api_endpoints.api_endpoints import APIEndpoints
from data.api_data import APIData
from data.home_page_data import HomePageData
from data.order_page_data import OrderPageData
import logging

logger = logging.getLogger(__name__)

class OrderPage:

    def __init__(self, browser_setup):
        self.page, self.api_context = browser_setup

    def create_order(self, shared_data):
        """ Create an Order """
        response = self.api_context.post(url=APIEndpoints.create_product_url, headers={"Content-Type": "application/json",
                                                                                  "Authorization": shared_data.get(
                                                                                      "token")},
                                    data={"orders": [{"country": APIData.create_order_country,
                                                      "productOrderedId": shared_data.get("item_id")}]})
        if not response.ok:
            raise ValueError(f"API Login failed [{response.status}]: {response.text()}")
        else:
            logger.info(f"Json response: {response.json()}")
        assert response.json().get(
            "message") == "Order Placed Successfully", f"Message: {response.json().get('message')}"
        shared_data["order_id"] = response.json().get("orders")[0]
        logger.info(f"Order ID: {shared_data['order_id']}")

    def navigate_to_order_page(self):
        """ Navigate to Order Page """
        self.page.locator(HomePageLocators.orders_menu_btn).filter(has_text="  ORDERS").click()

    def verify_order_id(self, shared_data):
        """ Verify Order ID """
        product_order_id = self.page.locator(OrderPageLocators.order_id_value).text_content()
        logger.info(f"Product Order ID: {product_order_id}")
        assert product_order_id == shared_data.get("order_id"), f"Order ID: {product_order_id}"

    def verify_product_name(self):
        """ Verify Product Name """
        product_name = self.page.locator(OrderPageLocators.product_name_value).text_content()
        logger.info(f"Product Name: {product_name}")
        assert product_name == HomePageData.adidas_product, f"Product Name: {product_name}"

    def verify_product_price(self, shared_data, product):
        """ Verify Product Price """
        product_price = self.page.locator(OrderPageLocators.product_price_value).text_content()
        logger.info(f"Product Price: {product_price}")
        assert product_price == shared_data.get(f"{product} price: "), f"Product Price: {product_price}"

    def click_delete_btn(self):
        """ Click on Delete Button """
        self.page.get_by_role("button", name="Delete").click()

    def verify_no_orders_msg(self):
        """ Verify No Orders Message """
        no_orders = self.page.locator(OrderPageLocators.no_order_msg).text_content()
        assert no_orders.strip() == OrderPageData.no_orders_msg, f"No Orders message: {no_orders}"
