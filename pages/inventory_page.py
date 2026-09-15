"""
InventoryPage class representing the product catalog page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from utils.config import EXPLICIT_WAIT


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

        # Locators
        self._title = (By.CSS_SELECTOR, ".title")
        self._product_names = (By.CSS_SELECTOR, ".inventory_item_name")
        self._product_prices = (By.CSS_SELECTOR, ".inventory_item_price")
        self._sort_select = (By.CSS_SELECTOR, ".product_sort_container")
        self._cart_icon = (By.CSS_SELECTOR, ".shopping_cart_link")
        self._cart_badge = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def is_on_inventory_page(self):
        """Verify that current page is the inventory catalog."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self._title))
            return element.text.lower() == "products" and "/inventory.html" in self.driver.current_url
        except Exception:
            return False

    def get_product_names(self):
        """Return list of all visible product names as strings."""
        self.wait.until(EC.presence_of_all_elements_located(self._product_names))
        elements = self.driver.find_elements(*self._product_names)
        return [elem.text.strip() for elem in elements]

    def get_product_prices(self):
        """Return list of all visible product prices as float values."""
        self.wait.until(EC.presence_of_all_elements_located(self._product_prices))
        elements = self.driver.find_elements(*self._product_prices)
        prices = []
        for elem in elements:
            clean_price = elem.text.replace("$", "").strip()
            prices.append(float(clean_price))
        return prices

    def add_product_to_cart(self, product_name):
        """Click 'Add to cart' button for a specific product by title."""
        xpath = f"//div[@class='inventory_item'][.//div[contains(@class,'inventory_item_name') and text()='{product_name}']]//button"
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()
        return self

    def open_cart(self):
        """Click the cart icon to navigate to the cart page."""
        cart = self.wait.until(EC.element_to_be_clickable(self._cart_icon))
        cart.click()
        return self

    def sort_products(self, sort_option):
        """
        Sort products using the sort dropdown.
        Options: 'az' (A to Z), 'za' (Z to A), 'lohi' (low to high), 'hilo' (high to low).
        """
        select_elem = self.wait.until(EC.element_to_be_clickable(self._sort_select))
        select = Select(select_elem)
        select.select_by_value(sort_option)
        return self

    def get_cart_badge_count(self):
        """Return the number displayed on the cart badge (0 if missing)."""
        elements = self.driver.find_elements(*self._cart_badge)
        if elements and elements[0].is_displayed():
            return int(elements[0].text)
        return 0
