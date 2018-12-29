from utils.webdriver import wait_element_presence, wait_all_elements_presence
from element_wrapper import Element, ElementList


class Region(object):
    def __init__(self, root):
        self._root = root

    def __cache__(self):
        pass

    def find_element(self, locator, element_class=None):
        _element = wait_element_presence(locator=locator, root=self._root, timeout=10)
        if element_class is not None:
            return element_class(element=_element)
        else:
            return Element(element=_element)

    def find_elements(self, locator, element_class=None):
        _elements = wait_all_elements_presence(locator=locator, root=self._root, timeout=10)
        if element_class is not None:
            return ElementList(elements=_elements, element_class=element_class)
        else:
            return ElementList(elements=_elements)

