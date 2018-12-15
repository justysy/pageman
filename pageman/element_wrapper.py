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

    def _execute_js_on_browser(self, browser_js, *args):
        driver = self._element.parent
        return driver.execute_script(browser_js, self._element, *args)

    def bind_browser_js(self, func_name, browser_js):
        setattr(self, func_name, functools.partial(self._execute_js_on_browser, browser_js))

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
