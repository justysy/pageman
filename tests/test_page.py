import unittest
import mock
from context import page


class TestPage(unittest.TestCase):
    def _init_sut(self):
        mock_driver = mock.Mock()
        self._mock_driver = mock_driver
        sut = page.Page(mock_driver)
        return sut

    def test_init(self):
        sut = self._init_sut()
        self.assertNotEqual(sut, None)

    @mock.patch('pageman.page.mouse_to_element')
    @mock.patch('pageman.page.reset_mouse_position')
    def test_hover(self, mock_reset_mouse, mock_mouse_to):
        sut = self._init_sut()
        mock_element = mock.Mock()
        with sut.hover(mock_element):
            pass
        actual_call_mouse_to = mock_mouse_to.call_args
        self.assertEqual(
            actual_call_mouse_to,
            mock.call(self._mock_driver, mock_element, None)
        )
        actual_call_reset_mouse = mock_reset_mouse.call_args
        self.assertEqual(
            actual_call_reset_mouse,
            mock.call(self._mock_driver)
        )



if __name__ == '__main__':
    unittest.main()
