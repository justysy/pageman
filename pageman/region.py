from selenium.common.exceptions import NoSuchElementException
from utils.webdriver import wait_element_presence, wait_all_elements_presence
from element_wrapper import Element, ElementList


class Region(object):
    def __init__(self, ancestor, presence_timeout=10):
        """
        :param ancestor: web driver/web element which starts to locate root
        :param presence_timeout: timeout for waiting element presence
        """
        self._ancestor = ancestor
        self._cache = dict()
        self.presence_timeout = presence_timeout
        try:
            _ = self.root
        except AttributeError:
            raise NotImplementedError('_root_locator')
        self._wait_for_ready()

    @property
    def root(self):
        return self.find_element(
            locator=self._root_locator,
            root=self._ancestor
        )

    def _wait_for_ready(self):
        return self.root is not None

    def _set_cache(self, key, value):
        self._cache[key] = value

    def set_presence_timeout(self, presence_timeout):
        self.presence_timeout = presence_timeout

    def check(self, element_name):
        original_presence_timeout = self.presence_timeout
        self.set_presence_timeout(.1)
        try:
            _ = getattr(self, element_name)
            if isinstance(_, ElementList):
                if len(_) == 0:
                    raise NoSuchElementException
            elif _ is None:
                raise NoSuchElementException
        finally:
            self.set_presence_timeout(original_presence_timeout)

    def find_element(self, locator, root=None, element_class=None, cacheable=True):
        if root is None:
            root = self.root
        cache_id = (locator, root, element_class)
        if cacheable:
            if cache_id in self._cache:
                return self._cache[cache_id]
        element = wait_element_presence(locator=locator, root=root, timeout=self.presence_timeout)
        if element_class is not None:
            element_wrapper = element_class(element=element)
        else:
            element_wrapper = Element(element=element)
        if cacheable:
            self._set_cache(cache_id, element_wrapper)
        return element_wrapper

    def find_elements(self, locator, root=None, element_class=None, cacheable=True):
        if root is None:
            root = self.root
        cache_id = (locator, root, element_class)
        if cacheable:
            if cache_id in self._cache:
                return self._cache[cache_id]
        elements = wait_all_elements_presence(locator=locator, root=root, timeout=self.presence_timeout)
        if element_class is not None:
            elements_wrapper = ElementList(elements=elements, element_class=element_class)
        else:
            elements_wrapper = ElementList(elements=elements)
        if cacheable:
            self._set_cache(cache_id, elements_wrapper)
        return elements_wrapper
