import unittest
import mock
from context import region


class TestRegion(unittest.TestCase):
    def _init_sut(self):
        self._mock_driver = mock.Mock()
        return region.Region(driver=self._mock_driver)

    def test_init(self):
        sut = self._init_sut()
        self.assertNotEqual(sut, None)

    @mock.patch('pageman.region.wait_element_presence')
    def test_find_element(self, mock_wait_presence):
        mock_element = mock.Mock()
        mock_wait_presence.return_value = mock_element
        sut = self._init_sut()
        actual = sut.find_element('<mock_locator>')
        self.assertEqual(actual.get_element(), mock_element)
        actual_call = mock_wait_presence.call_args
        expected_call = mock.call(locator='<mock_locator>', root=self._mock_driver, timeout=10)
        self.assertEqual(actual_call, expected_call)

    @mock.patch('pageman.region.wait_element_presence')
    def test_find_cached_element(self, mock_wait_presence):
        mock_element = mock.Mock()
        mock_wait_presence.return_value = mock_element
        sut = self._init_sut()
        actual = sut.find_element('<mock_locator>')
        self.assertEqual(actual.get_element(), mock_element)
        cache = sut.find_element('<mock_locator>')
        self.assertEqual(cache.get_element(), mock_element)
        actual_call_count = len(mock_wait_presence.call_args_list)
        self.assertEqual(actual_call_count, 1)

    @mock.patch('pageman.region.wait_all_elements_presence')
    def test_find_elements(self, mock_wait_all_presence):
        mock_element = mock.Mock()
        mock_wait_all_presence.return_value = [mock_element]
        sut = self._init_sut()
        actual = sut.find_elements('<mock_locator>')
        self.assertEqual(actual.get_elements(), [mock_element])
        actual_call = mock_wait_all_presence.call_args
        expected_call = mock.call(locator='<mock_locator>', root=self._mock_driver, timeout=10)
        self.assertEqual(actual_call, expected_call)

    @mock.patch('pageman.region.wait_all_elements_presence')
    def test_find_cache_elements(self, mock_wait_all_presence):
        mock_element = mock.Mock()
        mock_wait_all_presence.return_value = [mock_element]
        sut = self._init_sut()
        actual = sut.find_elements('<mock_locator>')
        self.assertEqual(actual.get_elements(), [mock_element])
        cached = sut.find_elements('<mock_locator>')
        self.assertEqual(cached.get_elements(), [mock_element])
        actual_call_count = len(mock_wait_all_presence.call_args_list)
        self.assertEqual(actual_call_count, 1)


if __name__ == '__main__':
    unittest.main()
