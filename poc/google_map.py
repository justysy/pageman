from selenium.webdriver.common.by import By
from pageman.region import Region


class SearchBoxContainer(Region):
    def __init__(self, driver):
        super(SearchBoxContainer, self).__init__(driver)
        self._root_locator = (By.ID, 'omnibox-container')

    def wait_for_ready(self):
        locator = (By.ID, 'omnibox-container')

