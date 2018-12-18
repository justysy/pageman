import time
import functools
from selenium.common.exceptions import WebDriverException, TimeoutException


class Element(object):
    def __init__(self, element):
        self._element = element

    def __getattr__(self, item):
        if hasattr(self._element, item):
            return getattr(self._element, item)
        else:
            raise AttributeError

    def execute_js_on_browser(self, browser_js, *args):
        driver = self._element.parent
        return driver.execute_script(browser_js, self._element, *args)

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
    def __init__(self, elements, element_class=Element):
        self._elements = elements
        self._element_class = element_class

    def __iter__(self):
        for element in self._elements:
            yield self._element_class(element)

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, index):
        return self._element_class(self._elements[index])

    def __add__(self, other):
        if self.get_element_class() != other.get_element_class():
            raise ElementListClassNotIdentical()
        return ElementList(self._elements + other.get_elements())

    def get_elements(self):
        return self._elements

    def get_element_class(self):
        return self._element_class


class ElementListClassNotIdentical(Exception):
    pass
