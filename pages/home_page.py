from config.config import Config
from locators.home_page_locators import HomePageLocators
from api_endpoints.api_endpoints import APIEndpoints
from data.api_data import APIData
from data.home_page_data import HomePageData
import logging

logger = logging.getLogger(__name__)

class HomePage:

    def __init__(self, browser_setup):
        self.page, self.api_context = browser_setup

    def navigate_to_home_page(self):
        """ Navigate to Home Page """
        self.page.goto(Config.HOME_PAGE_URL)
        logger.info(f"Page URL: {self.page.url}")

    def home_menu_display(self):
        """ Verify Home menu display """
        home = self.page.locator(HomePageLocators.home_menu_btn).text_content()
        logger.info(f"Home menu text: {home}")
        assert home.strip() == "HOME"

    def sign_out_display(self):
        """ Verify Sign out display """
        sign_out = self.page.locator(HomePageLocators.sign_out_btn).text_content()
        logger.info(f"Sign out text: {sign_out}")
        assert sign_out.strip() == "Sign Out"

    def get_all_product_api(self, shared_data):
        """ Get all Products API """
        response = self.api_context.post(url=APIEndpoints.get_all_products_url, headers={"Content-Type": "application/json",
                                                                                    "Authorization": shared_data.get(
                                                                                        "token")},
                                    data=APIData.get_all_products_payload)
        if not response.ok:
            raise ValueError(f"API Login failed [{response.status}]: {response.text()}")
        else:
            logger.info(f"Json response: {response.json()}")
        shared_data["item_id"] = response.json().get("data")[0].get("_id")
        logger.info(f"Item ID: {shared_data['item_id']}")

    def add_product_to_cart(self, shared_data, product):
        """ Add product to cart """
        item1 = self.page.locator(HomePageLocators.home_page_products).filter(has_text=product)
        shared_data[f"{product} price: "] = item1.locator("//div[@class='text-muted']").text_content()
        logger.info(f"{HomePageData.adidas_product} price: {shared_data.get(f"{product} price: ")}")
        item1.locator("//button").filter(has_text=" Add To Cart").click()

