"""
CartPage class representing the shopping cart page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import EXPLICIT_WAIT


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

        # Locators
        self._title = (By.CSS_SELECTOR, ".title")
        self._cart_items = (By.CSS_SELECTOR, ".cart_item")
        self._item_names = (By.CSS_SELECTOR, ".inventory_item_name")
        self._checkout_button = (By.ID, "checkout")

    def is_on_cart_page(self):
        """Verify navigation to the Cart page with explicit wait."""
        try:
            self.wait.until(EC.url_contains("/cart.html"))
            element = self.wait.until(EC.visibility_of_element_located(self._title))
            return "your cart" in element.text.lower()
        except Exception:
            return False

    def get_cart_items(self):
        """Return list of item names present in the cart."""
        self.wait.until(EC.presence_of_all_elements_located(self._item_names))
        elements = self.driver.find_elements(*self._item_names)
        return [elem.text.strip() for elem in elements]

    def remove_product(self, product_name):
        """Remove a product from cart by product name."""
        xpath = f"//div[@class='cart_item'][.//div[contains(@class,'inventory_item_name') and normalize-space(text())='{product_name}']]//button"
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()
        return self

    def checkout(self):
        """Click checkout button."""
        button = self.wait.until(EC.element_to_be_clickable(self._checkout_button))
        button.click()
        return self

    def is_cart_empty(self):
        """Check if cart contains 0 items."""
        items = self.driver.find_elements(*self._cart_items)
        return len(items) == 0
