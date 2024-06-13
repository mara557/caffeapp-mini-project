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



# Overall Structure

# Importing Necessary Modules:
# unittest: The core library for unit testing in Python.
# unittest.mock.patch: A utility to replace functions and objects in tests with mock objects.
# get_valid_input from src.app: The function being tested.

# Test Class:
# TestCafeApp is a subclass of unittest.TestCase, which groups the test methods.
# Individual Test Methods

# test_get_valid_input_str:
# Purpose: To test if get_valid_input correctly handles string input.
# Mocked Input: 'valid_name'
# Expected Result: The function should return 'valid_name'.

# test_get_valid_input_int:
# Purpose: To test if get_valid_input correctly converts a valid integer string to an integer.
# Mocked Input: '5'
# Expected Result: The function should return 5.

# test_get_valid_input_invalid_int:
# Purpose: To test if get_valid_input handles invalid integer input and retries until a valid integer is provided.
# Mocked Inputs: 'invalid' followed by '5'
# Expected Result: The function should retry on invalid input and eventually return 5.

# test_get_valid_input_with_pattern:
# Purpose: To test if get_valid_input validates the input against a provided regex pattern.
# Mocked Inputs: '123abc' (invalid as per pattern) followed by '456' (valid as per pattern)
# Pattern: r'^\d+$' (expects only digits)
# Expected Result: The function should return '456'.

# test_get_valid_input_allow_empty:
# Purpose: To test if get_valid_input allows an empty input when allow_empty is set to True.
# Mocked Input: ''
# Expected Result: The function should return ''.