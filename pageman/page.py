from contextlib import contextmanager
from utils.webdriver import mouse_to_element, reset_mouse_position


class Page(object):
    def __init__(self, driver):
        self._driver = driver
        pass

    def _mouse_to_element(self, element, offset):
        mouse_to_element(self._driver, element, offset)

    def _reset_mouse_position(self):
        reset_mouse_position(self._driver)

    @contextmanager
    def hover(self, element, offset=None):
        self._mouse_to_element(element, offset)
        yield
        self._reset_mouse_position()
