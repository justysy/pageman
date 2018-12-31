from utils.webdriver import wait_element_presence, wait_all_elements_presence
from element_wrapper import Element, ElementList


class Region(object):
    def __init__(self, root):
        self._root = root
        self._cache = dict()

    def wait_for_ready(self):
        return False

    def _set_cache(self, key, value):
        self._cache[key] = value

    def find_element(self, locator, element_class=None, cacheable=True):
        if locator in self._cache:
            return self._cache[locator]
        _element = wait_element_presence(locator=locator, root=self._root, timeout=10)
        _element_wrapper = None
        if element_class is not None:
            _element_wrapper = element_class(element=_element)
        else:
            _element_wrapper = Element(element=_element)
        if cacheable:
            self._set_cache(locator, _element_wrapper)
        return _element_wrapper

    def find_elements(self, locator, element_class=None, cacheable=True):
        if locator in self._cache:
            return self._cache[locator]
        _elements = wait_all_elements_presence(locator=locator, root=self._root, timeout=10)
        _elements_wrapper = None
        if element_class is not None:
            _elements_wrapper = ElementList(elements=_elements, element_class=element_class)
        else:
            _elements_wrapper = ElementList(elements=_elements)
        if cacheable:
            self._set_cache(locator, _elements_wrapper)
        return _elements_wrapper
