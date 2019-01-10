import unittest
import mock
from context import element_wrapper


class TestElement(unittest.TestCase):
    def _init_sut(self, *args, **kargs):
        return element_wrapper.Element(*args, **kargs)

    def test_init(self):
        element = mock.Mock()
        sut = self._init_sut(element)
        self.assertTrue(sut)

    def test_redirect_function_to_wrapped(self):
        element = mock.Mock()
        element.wrapped_test_func.return_value = 'PASS'
        sut = self._init_sut(element)
        actual = sut.wrapped_test_func()
        self.assertEqual(actual, 'PASS')

    def test_click(self):
        element = mock.Mock()
        sut = self._init_sut(element)
        sut.click()
        self.assertTrue(element.click.called)

    @mock.patch('time.time')
    def test_click_retry(self, mock_time):
        element = mock.Mock()
        exceptions_to_be_raised = iter([element_wrapper.WebDriverException])

        def get_exception():
            while True:
                yield next(exceptions_to_be_raised)
        exception_gen = get_exception()

        def mock_click():
            try:
                exception_to_be_raised = next(exception_gen)
                raise exception_to_be_raised
            except StopIteration:
                pass
        element.click.side_effect = mock_click
        sut = self._init_sut(element)
        sut.click()
        actual = element.click.call_args_list
        expect = [mock.call(), mock.call()]
        self.assertEqual(actual, expect)

    @mock.patch('time.time')
    @mock.patch('time.sleep')
    def test_click_retry_to_timeout(self, mock_sleep, mock_time):
        element = mock.Mock()
        element.click.side_effect = element_wrapper.WebDriverException

        def time_time():
            time = 1
            while True:
                yield time
                time += 5
        time_gen = time_time()

        def mock_time_call():
            return next(time_gen)
        mock_time.side_effect = mock_time_call

        sut = self._init_sut(element)
        self.assertRaises(element_wrapper.TimeoutException, sut.click)

    def test_bind_browser_js(self):
        element = mock.Mock()
        element.parent = mock.Mock()

        sut = self._init_sut(element)
        sut.execute_js_on_browser('<test_mock_js>', 'arg1', 'arg2')

        expect = mock.call('<test_mock_js>', element, 'arg1', 'arg2')
        actual = element.parent.execute_script.call_args
        self.assertEqual(actual, expect)


class TestElementList(unittest.TestCase):
    def _init_sut(self, *args, **kargs):
        return element_wrapper.ElementList(*args, **kargs)

    def test_init(self):
        elements = [mock.Mock()]
        sut = self._init_sut(elements)
        self.assertTrue(sut)

    def test_iter(self):
        mock_element = mock.Mock()
        elements = [mock_element]
        sut = self._init_sut(elements)
        for item in sut:
            self.assertEqual(mock_element, item._element)

    def test_getitem(self):
        mock_element = mock.Mock()
        elements = [mock_element]
        sut = self._init_sut(elements)
        self.assertEqual(mock_element, sut[0]._element)

    def test_get_first(self):
        mock_element = mock.Mock()
        elements = [mock_element]
        sut = self._init_sut(elements)
        self.assertEqual(mock_element, sut.first()._element)

    def test_add(self):
        elements_1 = [mock.Mock()]
        elements_2 = [mock.Mock(), mock.Mock()]
        sut_1 = self._init_sut(elements_1)
        sut_2 = self._init_sut(elements_2)
        sut_1 += sut_2
        self.assertEqual(len(sut_1), 3)

    def test_search(self):
        mock_element_text = mock.Mock()
        mock_element_text.text = 'mock_text'
        mock_element_class = mock.Mock()
        mock_element_class.text = 'mock_class'
        mock_element_style = mock.Mock()
        mock_element_style.text = 'mock_style'

        def mock_get_attribute(key):
            return 'mock_attr_' + key

        mock_element_text.get_attribute.side_effect = mock_get_attribute
        mock_element_class.get_attribute.side_effect = mock_get_attribute

        def mock_get_attribute_style(_):
            return 'mock_attr_style_target'

        mock_element_style.get_attribute.side_effect = mock_get_attribute_style
        elements = [mock_element_text, mock_element_class, mock_element_style]
        sut = self._init_sut(elements)

        acutal_text = sut.search(text='text')
        self.assertEqual(acutal_text.get_elements(), [mock_element_text])
        actual_all = sut.search(class_='attr_class')
        self.assertEqual(actual_all.get_elements(), [mock_element_text, mock_element_class])
        actual_style = sut.search(style='attr_style_target')
        self.assertEqual(actual_style.get_elements(), [mock_element_style])


if __name__ == '__main__':
    unittest.main()
