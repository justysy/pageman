import time
from selenium.common.exceptions import WebDriverException, TimeoutException


class Element(object):
    def __init__(self, element):
        self._element = element

    def __getattr__(self, item):
        if hasattr(self._element, item):
            return getattr(self._element, item)
        else:
            raise AttributeError

    def click(self, timeout=5):
        start = time.time()
        while True:
            try:
                self._element.click()
                break
            except WebDriverException:
                time.sleep(.5)
            if time.time() - start > timeout:
                raise TimeoutException


class ElementNotFound(Exception):
    pass


class ElementList(object):
    def __init__(self, elements):
        self._elements = elements
