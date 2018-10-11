from contextlib import contextmanager
from webdriver_utils import reset_mouse_position, mouse_to_element
from locate_engine import LocateEngine


class Page(object):
    def __init__(self, driver):
        self._driver = driver
        self._engine = LocateEngine(driver)

    def check_ready(self):
        self._engine.is_ready()

    def _reset_mouse_position(self):
        reset_mouse_position(self._driver)

    def _hover_to(self, element, xoffset, yoffset):
        mouse_to_element(self._driver, element, xoffset, yoffset)

    @contextmanager
    def hover(self, element, xoffset=0, yoffset=0):
        self._hover_to(element, xoffset, yoffset)
        yield
        self._reset_mouse_position()
