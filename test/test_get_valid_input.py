import unittest
from unittest.mock import patch
from src.app import get_valid_input

class TestCafeApp(unittest.TestCase):

    def test_get_valid_input_str(self):
        with patch('builtins.input', side_effect=['valid_name']):
            result = get_valid_input(str, "Enter name: ", "Invalid input.")
            self.assertEqual(result, 'valid_name')

    def test_get_valid_input_int(self):
        with patch('builtins.input', side_effect=['5']):
            result = get_valid_input(int, "Enter number: ", "Invalid input.")
            self.assertEqual(result, 5)

    def test_get_valid_input_invalid_int(self):
        with patch('builtins.input', side_effect=['invalid', '5']):
            result = get_valid_input(int, "Enter number: ", "Invalid input.")
            self.assertEqual(result, 5)

    def test_get_valid_input_with_pattern(self):
        with patch('builtins.input', side_effect=['123abc', '456']):
            result = get_valid_input(str, "Enter number: ", "Invalid input.", pattern=r'^\d+$')
            self.assertEqual(result, '456')

    def test_get_valid_input_allow_empty(self):
        with patch('builtins.input', side_effect=['']):
            result = get_valid_input(str, "Enter name: ", "Invalid input.", allow_empty=True)
            self.assertEqual(result, '')

if __name__ == '__main__':
    unittest.main()