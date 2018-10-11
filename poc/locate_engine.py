import time
import re
import json
from webdriver_utils import mouse_to_element, wait_element_presence, get_svg_path_point_at_length, \
    wait_all_elements_presence, wait_element_clickable, expand_shadow_element, get_svg_path_total_length
from selenium.common.exceptions import TimeoutException, WebDriverException


class Element(object):
    def __init__(self, element):
        self._element = element

    def __getattr__(self, item):
        if hasattr(self._element, item):
            return getattr(self._element, item)
        else:
            raise AttributeError

    def __hash__(self):
        return hash(self._element)

    def get_svg_path_point(self, percent):
        total = get_svg_path_total_length(self._element)
        # print 'svg path total: ', total
        length = total * percent / 100.
        # print 'svg path point: ', length
        return get_svg_path_point_at_length(self._element, length)

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

    def __iter__(self):
        for element in self._elements:
            yield Element(element)

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, index):
        return Element(self._elements[index])

    def __add__(self, other):
        return ElementList(self._elements + other.get_elements())

    def get_elements(self):
        return self._elements

    def search(self, locator=None, **kwargs):
        key, value = list(kwargs.iteritems())[0]  # should contains only 1 item
        for element in self._elements:
            if locator is not None:
                _element = wait_element_presence(locator=locator, root=element, timeout=10)
            else:
                _element = element
            if key.endswith('_'):
                key = key[:-1]
            if key == 'text':
                element_value = _element.text
            else:
                element_value = _element.get_attribute(key)
            if re.search(value, element_value):
                found = element
                break
        else:
            raise ElementNotFound('kwargs: {0} not found in {1}'
                                  .format(kwargs, [element.get_attribute(key) for element in self._elements]))
        return Element(found)

    def search_list(self, locator=None, **kwargs):
        """
        :param locator:
            locator for locating child element inside each list element
        :param kwargs:
            search criteria, using regular expression
        :return:
        """
        found = []
        key, value = list(kwargs.iteritems())[0]  # should contains only 1 item
        for element in self._elements:
            if locator is not None:
                _element = wait_element_presence(locator=locator, root=element, timeout=10)
            else:
                _element = element
            if key.endswith('_'):
                key = key[:-1]
            if key == 'text':
                element_value = _element.text
            else:
                element_value = _element.get_attribute(key)
            if re.search(value, element_value):
                found.append(element)
        return ElementList(found)

    def search_indices(self, locator=None, **kwargs):
        """
        :param locator:
            locator for locating child element inside each list element
        :param kwargs:
            search criteria, using regular expression
        :return:
        """
        found = []
        key, value = list(kwargs.iteritems())[0]  # should contains only 1 item
        for idx, element in enumerate(self._elements):
            if locator is not None:
                _element = wait_element_presence(locator=locator, root=element, timeout=10)
            else:
                _element = element
            if key.endswith('_'):
                key = key[:-1]
            if key == 'text':
                element_value = _element.text
            else:
                element_value = _element.get_attribute(key)
            if re.search(value, element_value):
                found.append(idx)
        return found


class LocateCallable(object):
    def __init__(self, engine, locator, cacheable):
        self._cacheable = cacheable
        self._locator = locator
        self._engine = engine
        self._driver = engine.get_driver()

    def __call__(self, root=None):
        raise NotImplementedError()

    def _filter(self, element_list, action, action_kwargs):
        element = None
        if action == 'search':
            element = element_list.search(**action_kwargs)
        elif action == 'search_list':
            element = element_list.search_list(**action_kwargs)
        return element

    def _expand(self, entry, capsulation):
        new_root = None
        if capsulation == 'shadow':
            new_root = expand_shadow_element(self._driver, entry)
        elif capsulation == 'iframe':
            pass
        return new_root

    def _trigger(self, actor, action, action_kwargs=None):
        if action == 'click':
            actor.click()
        elif action == 'hover':
            mouse_to_element(self._driver, actor)
        elif action == 'drag_drop':
            pass
            # Not implemented yet
            # drag_drop(self._driver, actor, **action_kwargs)

    def _get_parent(self, parent_name, **kwargs):
        if parent_name is not None:
            element_parent = getattr(self._engine, parent_name)(**kwargs)
        else:
            element_parent = self._driver
        return element_parent

    def _process_parent(self, parent, timeout=5):
        try:
            parent_name = parent['name']
            _parent = self._get_parent(parent_name)
        except AttributeError:
            # parent should be an element
            _parent = parent
        if 'filter' in parent:
            action = parent['filter']['action']
            kwargs = parent['filter'].get('action_kwargs', {})
            start = time.time()
            while True:
                try:
                    parent_element = self._filter(_parent, action, kwargs)
                    break
                except ElementNotFound:
                    _parent = self._get_parent(parent_name, cache=False)
                if time.time() - start > timeout:
                    raise TimeoutException(parent_name)
        elif 'expand' in parent:
            capsulation = parent['expand']['capsulation']
            parent_element = self._expand(_parent, capsulation)
        else:
            parent_element = _parent
        return parent_element

    def _process_dependency(self, depend):
        actor_name, action_spec = depend.items()[0]
        action = action_spec['action']
        actor = getattr(self._engine, actor_name)(wait=action)
        action_kwargs = action_spec.get('action_kwargs', None)
        self._trigger(actor=actor, action=action, action_kwargs=action_kwargs)


class ElementLocateFunc(LocateCallable):
    def __init__(self, engine, locator, cacheable=True):
        super(ElementLocateFunc, self).__init__(engine, locator, cacheable)

    def __call__(self, ondemand_root=None, wait='presence', cache=None, timeout=10):
        try:
            _element = self.locate_element(self._locator, ondemand_root, wait, cache, timeout)
            return Element(_element)
        except:
            print('Failed to locate element: {0}'.format(self._locator))
            raise

    def locate_element(self, locator, ondemand_root, wait, cache, timeout):
        if cache is None:
            try:
                return self._locate_element(locator, ondemand_root, wait, cache=True, timeout=timeout)
            except (TimeoutException, ElementNotFound):
                if self._cacheable:
                    return self._locate_element(locator, ondemand_root, wait, cache=False, timeout=timeout)
                else:
                    raise
        else:
            return self._locate_element(locator, ondemand_root, wait, cache, timeout)

    def _locate_element(self, locator, ondemand_root, wait, cache, timeout):
        """
        :param locator:
        example: locator = {
            'location': (By.CSS_SELECTOR, 'input#userName'),
            'parent': {
                'name': 'parent name'.
                'filter': {
                    'action': 'search',
                    'action_kwargs': kwargs
                    },
                },
            'trigger': {
                'actor locator name': [{'action': 'click|hover|search', 'action_kwargs': {...}}, ...]
                }
            }
        example: locator = 'username'
        :param ondemand_root:
        :param cache:
        :return: selenium web element
        """
        # cache
        locator_key = json.dumps(locator, sort_keys=True)
        if cache and locator_key in self._engine.__cache__:
            # print('hit cache: {0}'.format(locator_key))
            return self._engine.__cache__[locator_key]

        # determine root
        if ondemand_root is None:
            root = self._process_parent(locator['parent'])
        else:
            root = ondemand_root

        # do trigger
        if 'trigger' in locator:
            self._process_dependency(locator['trigger'])

        # find the element
        if locator['location'] is None:
            element = root
        else:
            if wait == 'click':
                element = wait_element_clickable(locator['location'], root, timeout)
            else:
                element = wait_element_presence(locator['location'], root, timeout)
        if self._cacheable:
            self._engine.set_cache(locator_key, element)
        return element


class ListLocateFunc(LocateCallable):
    def __init__(self, engine, locator, cacheable=True):
        super(ListLocateFunc, self).__init__(engine, locator, cacheable)

    def __call__(self, ondemand_root=None, cache=None, timeout=10):
        try:
            elements = self.locate_element_list(self._locator, ondemand_root, cache, timeout)
            return ElementList(elements)
        except (TimeoutException, ElementNotFound):
            return ElementList([])

    def locate_element_list(self, locator, ondemand_root, cache, timeout):
        if cache is None:
            try:
                return self._locate_element_list(locator, ondemand_root, cache=True, timeout=timeout)
            except (TimeoutException, ElementNotFound):
                if self._cacheable:
                    return self._locate_element_list(locator, ondemand_root, cache=False, timeout=timeout)
                else:
                    raise
        else:
            return self._locate_element_list(locator, ondemand_root, cache, timeout)

    def _locate_element_list(self, locator, ondemand_root, cache, timeout):
        """
        :param locator:
        example: locator = {
            'location': (By.CSS_SELECTOR, 'input#userName'),
            'parent': {
                'name': 'parent name'.
                'filter': {
                    'action': 'search',
                    'action_kwargs': kwargs
                    },
                },
            'trigger': {
                'actor locator name': [{'action': 'click|hover|search', 'action_kwargs': {...}}, ...]
                }
            }
        example: locator = 'username'
        :param ondemand_root:
        :param cache:
        :return: web element list
        """
        # cache
        locator_key = json.dumps(locator, sort_keys=True)
        if cache and locator_key in self._engine.__cache__:
            # print('hit cache: {0}'.format(locator_key))
            return self._engine.__cache__[locator_key]

        # determine root
        if ondemand_root is None:
            root = self._process_parent(locator['parent'])
        else:
            root = ondemand_root

        # do trigger
        if 'trigger' in locator:
            self._process_dependency(locator['trigger'])

        # find elements
        elements = wait_all_elements_presence(locator['location'], root, timeout)
        if self._cacheable:
            self._engine.set_cache(locator_key, elements)
        return elements


class LocateEngine(object):
    def __init__(self, driver, parent=None, ancestor=None, locators=None):
        """
        :param driver: selenium web driver
        :param parent: dict({
            'name': 'parent name'.
            'filter': {
                'action': 'search',
                'action_kwargs': kwargs
                },
            })
        :param ancestor: dict({
            'location': 'ancestor name'.
            })
        :param locators: dict({
            'locate_callable_name': locator,
            ...
        })
        """
        self._driver = driver
        self._parent = {'name': parent}
        self._trigger = None
        self._ancestor = ancestor
        if locators is None:
            self._locators = {'__cache__': {}}
        else:
            self._locators = locators

    def __getattr__(self, item):
        if item in self._locators:
            return self._locators[item]
        else:
            raise AttributeError

    def set_parent(self, parent_name):
        return LocateEngine(self._driver, parent_name, None, self._locators)

    def set_cache(self, key, value):
        self._locators['__cache__'][key] = value

    def get_driver(self):
        return self._driver

    def get_locators(self):
        return self._locators

    def add_element(self, name, location=None, trigger=None, cacheable=True):
        locator = {
            'location': location,
            'parent': self._parent
        }
        if self._trigger is not None:
            locator['trigger'] = self._trigger
        if trigger is not None:
            locator_trigger = locator.setdefault('trigger', {})
            locator_trigger.update(trigger)
        self._locators[name] = ElementLocateFunc(self, locator, cacheable)
        return LocateEngine(self._driver, name, self._parent['name'], self._locators)

    def add_list(self, name, location=None, trigger=None, cacheable=True):
        locator = {
            'location': location,
            'parent': self._parent
        }
        if self._trigger is not None:
            locator['trigger'] = self._trigger
        if trigger is not None:
            locator_trigger = locator.setdefault('trigger', {})
            locator_trigger.update(trigger)
        self._locators[name] = ListLocateFunc(self, locator, cacheable)
        return LocateEngine(self._driver, name, self._parent['name'], self._locators)

    def click(self):
        if self._trigger is None:
            self._trigger = dict()
        action = self._trigger.setdefault(self._parent['name'], {})
        action['action'] = 'click'
        return self

    def hover(self):
        if self._trigger is None:
            self._trigger = dict()
        action = self._trigger.setdefault(self._parent['name'], {})
        action['action'] = 'hover'
        return self

    def search(self, **kwargs):
        parent_filter = self._parent.setdefault('filter', {})
        parent_filter['action'] = 'search'
        parent_filter['action_kwargs'] = kwargs
        return self

    def sibling(self):
        if self._ancestor is None:
            raise Exception('Should not use multiple sibling calls.')
        return LocateEngine(self._driver, self._ancestor, None, self._locators)

    def shadow(self):
        parent_expand = self._parent.setdefault('expand', {})
        parent_expand['capsulation'] = 'shadow'
        return self

    @staticmethod
    def _create_static_trigger(location_name, action, action_kwargs=None):
        trigger = {location_name: {'action': action}}
        if action_kwargs is not None:
            trigger[location_name]['action_kwargs'] = action_kwargs
        return trigger

    def by_click(self, location_name):
        return self._create_static_trigger(location_name, 'click')
