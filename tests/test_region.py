import unittest
import mock
from context import region


class TestRegion(unittest.TestCase):
    def _init(self):
        self._mock_root = mock.Mock()
        return region.Region(root=self._mock_root)

    def test_init(self):
        sut = self._init()
        self.assertNotEqual(sut, None)

    @mock.patch('pageman.region.wait_element_presence')
    def test_find_element(self, mock_wait_presence):
        mock_element = mock.Mock()
        mock_wait_presence.return_value = mock_element
        sut = self._init()
        actual = sut.find_element('<mock_locator>')
        actual_call = mock_wait_presence.call_args
        expected_call = mock.call(locator='<mock_locator>', root=self._mock_root, timeout=10)
        self.assertEqual(actual.get_element(), mock_element)
        self.assertEqual(actual_call, expected_call)

    @mock.patch('pageman.region.wait_all_elements_presence')
    def test_find_elements(self, mock_wait_all_presence):
        mock_element = mock.Mock()
        mock_wait_all_presence.return_value = [mock_element]
        sut = self._init()
        actual = sut.find_elements('<mock_locator>')
        actual_call = mock_wait_all_presence.call_args
        expected_call = mock.call(locator='<mock_locator>', root=self._mock_root, timeout=10)
        self.assertEqual(actual.get_elements(), [mock_element])
        self.assertEqual(actual_call, expected_call)


if __name__ == '__main__':
    unittest.main()
