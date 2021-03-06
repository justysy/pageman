import unittest
import mock
from selenium.common.exceptions import NoSuchElementException
from context import region


class RegionForTest(region.Region):
    def __init__(self, ancestor):
        self._root_locator = '<mock_root_locator>'
        super(RegionForTest, self).__init__(ancestor)

    @property
    def test_element(self):
        locator = '<mock_locator>'
        return self.find_element(locator)

    @property
    def test_element_list(self):
        locator = '<mock_locator>'
        return self.find_elements(locator)


class TestRegion(unittest.TestCase):
    def _init_sut(self):
        self._mock_driver = mock.Mock()
        sut = RegionForTest(self._mock_driver)
        return sut

    def test_init(self):
        sut = self._init_sut()
        self.assertNotEqual(sut, None)

    @mock.patch('pageman.region.wait_element_presence')
    def test_check_element(self, mock_wait_presence):
        mock_element = mock.Mock()
        mock_wait_presence.return_value = mock_element
        sut = self._init_sut()
        sut.check('test_element')
        actual_calls = mock_wait_presence.call_args_list
        expected_calls = [
            mock.call(locator='<mock_root_locator>', root=self._mock_driver, timeout=10),
            mock.call(locator='<mock_locator>', root=sut.root, timeout=.1)
        ]
        self.assertEqual(actual_calls, expected_calls)

    @mock.patch('pageman.region.wait_element_presence')
    @mock.patch('pageman.region.wait_all_elements_presence')
    def test_check_elements(self, mock_wait_all_presence, mock_wait_presence):
        mock_element = mock.Mock()
        mock_wait_presence.return_value = mock_element
        mock_wait_all_presence.return_value = []
        sut = self._init_sut()
        with self.assertRaises(NoSuchElementException):
            sut.check('test_element_list')
        actual_calls = mock_wait_all_presence.call_args_list
        expected_calls = [
            mock.call(locator='<mock_locator>', root=sut.root, timeout=.1)
        ]
        self.assertEqual(actual_calls, expected_calls)

    @mock.patch('pageman.region.wait_element_presence')
    def test_find_element(self, mock_wait_presence):
        mock_element = mock.Mock()
        mock_wait_presence.return_value = mock_element
        sut = self._init_sut()
        actual = sut.find_element('<mock_locator>')
        self.assertEqual(actual.get_element(), mock_element)
        actual_calls = mock_wait_presence.call_args_list
        expected_calls = [
            mock.call(locator='<mock_root_locator>', root=self._mock_driver, timeout=10),
            mock.call(locator='<mock_locator>', root=sut.root, timeout=10)
        ]
        self.assertEqual(actual_calls, expected_calls)

    @mock.patch('pageman.region.wait_element_presence')
    def test_find_cached_element(self, mock_wait_presence):
        mock_element = mock.Mock()
        mock_wait_presence.return_value = mock_element
        sut = self._init_sut()
        actual = sut.find_element('<mock_locator>')  # access
        self.assertEqual(actual.get_element(), mock_element)
        cache = sut.find_element('<mock_locator>')   # access cache
        self.assertEqual(cache.get_element(), mock_element)
        actual_calls = mock_wait_presence.call_args_list
        expected_calls = [
            mock.call(locator='<mock_root_locator>', root=self._mock_driver, timeout=10),
            mock.call(locator='<mock_locator>', root=sut.root, timeout=10)
        ]
        self.assertEqual(actual_calls, expected_calls)

    @mock.patch('pageman.region.wait_element_presence')
    @mock.patch('pageman.region.wait_all_elements_presence')
    def test_find_elements(self, mock_wait_all_presence, mock_wait_presence):
        mock_element = mock.Mock()
        mock_wait_all_presence.return_value = [mock_element]
        sut = self._init_sut()
        actual = sut.find_elements('<mock_locator>')
        self.assertEqual(actual.get_elements(), [mock_element])
        actual_calls = mock_wait_all_presence.call_args_list
        expected_calls = [
            mock.call(locator='<mock_locator>', root=sut.root, timeout=10)
        ]
        self.assertEqual(actual_calls, expected_calls)
        actual_calls = mock_wait_all_presence.call_args_list
        expected_calls = [
            mock.call(locator='<mock_locator>', root=sut.root, timeout=10)
        ]
        self.assertEqual(actual_calls, expected_calls)

    @mock.patch('pageman.region.wait_element_presence')
    @mock.patch('pageman.region.wait_all_elements_presence')
    def test_find_cache_elements(self, mock_wait_all_presence, mock_wait_presence):
        mock_element = mock.Mock()
        mock_wait_all_presence.return_value = [mock_element]
        sut = self._init_sut()
        actual = sut.find_elements('<mock_locator>')
        self.assertEqual(actual.get_elements(), [mock_element])
        cached = sut.find_elements('<mock_locator>')
        self.assertEqual(cached.get_elements(), [mock_element])
        actual_calls = mock_wait_all_presence.call_args_list
        expected_calls = [
            mock.call(locator='<mock_locator>', root=sut.root, timeout=10)
        ]
        self.assertEqual(actual_calls, expected_calls)
        self.assertEqual(actual.get_elements(), [mock_element])
        actual_calls = mock_wait_all_presence.call_args_list
        expected_calls = [
            mock.call(locator='<mock_locator>', root=sut.root, timeout=10)
        ]
        self.assertEqual(actual_calls, expected_calls)

    def test_root_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            _ = region.Region(mock.Mock())

    @mock.patch('pageman.region.wait_element_presence')
    def test_set_presence_timeout(self, mock_wait_presence):
        mock_element = mock.Mock()
        mock_wait_presence.return_value = mock_element
        sut = self._init_sut()
        sut.set_presence_timeout(5)
        actual = sut.find_element('<mock_locator>')
        self.assertEqual(actual.get_element(), mock_element)
        actual_calls = mock_wait_presence.call_args_list
        expected_calls = [
            mock.call(locator='<mock_root_locator>', root=self._mock_driver, timeout=10),
            mock.call(locator='<mock_locator>', root=sut.root, timeout=5)
        ]
        self.assertEqual(actual_calls, expected_calls)


if __name__ == '__main__':
    unittest.main()
