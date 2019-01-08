from utils.webdriver import wait_element_presence, wait_all_elements_presence
from element_wrapper import Element, ElementList


class Region(object):
    def __init__(self, driver):
        self._driver = driver
        self._cache = dict()
        self._root_locator = None
        self.wait_for_ready()

    @property
    def root(self):
        if self._root_locator is None:
            raise NotImplementedError
        return self.find_element(
            locator=self._root_locator,
            root=self._driver
        )

    def wait_for_ready(self):
        pass

    def _set_cache(self, key, value):
        self._cache[key] = value

    def find_element(self, locator, root=None, element_class=None, cacheable=True):
        if root is None:
            root = self.root
        if locator in self._cache:
            return self._cache[locator]
        element = wait_element_presence(locator=locator, root=root, timeout=10)
        if element_class is not None:
            element_wrapper = element_class(element=element)
        else:
            element_wrapper = Element(element=element)
        if cacheable:
            self._set_cache(locator, element_wrapper)
        return element_wrapper

    def find_elements(self, locator, root=None, element_class=None, cacheable=True):
        if root is None:
            root = self.root
        if locator in self._cache:
            return self._cache[locator]
        elements = wait_all_elements_presence(locator=locator, root=root, timeout=10)
        if element_class is not None:
            elements_wrapper = ElementList(elements=elements, element_class=element_class)
        else:
            elements_wrapper = ElementList(elements=elements)
        if cacheable:
            self._set_cache(locator, elements_wrapper)
        return elements_wrapper
