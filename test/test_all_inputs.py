import unittest  
from unittest.mock import patch  
from src.app import get_valid_input  
from src.app import CafeApp


class TestCafeApp(unittest.TestCase):  # Define a test case class that inherits from unittest.TestCase

    @patch('builtins.input', side_effect=['1'])
    def test_get_valid_input_valid_integer(self, mock_input):
        """
        Test get_valid_input with a valid integer input.
        """
        # Arrange
        prompt = "Enter a number: "
        error_message = "Invalid input."
        
        # Act
        result = get_valid_input(int, prompt, error_message)
        
        # Assert
        self.assertEqual(result, 1)  # Check if the result is 1

    @patch('builtins.input', side_effect=['a', '1'])
    def test_get_valid_input_invalid_then_valid_integer(self, mock_input):
        """
        Test get_valid_input with an invalid input followed by a valid input.
        """
        # Arrange
        prompt = "Enter a number: "
        error_message = "Invalid input."
        
        # Act
        result = get_valid_input(int, prompt, error_message)
        
        # Assert
        self.assertEqual(result, 1)  # Check if the result is 1

    @patch('builtins.input', side_effect=[''])
    def test_get_valid_input_empty_with_default(self, mock_input):
        """
        Test get_valid_input with an empty input and default value allowed.
        """
        # Arrange
        prompt = "Enter something: "
        error_message = "Invalid input."
        default_value = "default"
        allow_empty = True
        
        # Act
        result = get_valid_input(str, prompt, error_message, default_value=default_value, allow_empty=allow_empty)
        
        # Assert
        self.assertEqual(result, default_value)  # Check if the result is the default value

    @patch('builtins.input', side_effect=['invalid-email', 'test@example.com'])
    def test_get_valid_input_pattern_matching(self, mock_input):
        """
        Test get_valid_input with a pattern for email validation.
        """
        # Arrange
        prompt = "Enter email: "
        error_message = "Invalid email."
        pattern = r'^\S+@\S+\.\S+$'
        
        # Act
        result = get_valid_input(str, prompt, error_message, pattern=pattern)
        
        # Assert
        self.assertEqual(result, 'test@example.com')  # Check if the result matches the valid email

    @patch('builtins.input', side_effect=['invalid-phone', '+1234567890'])
    def test_get_valid_input_phone_pattern_matching(self, mock_input):
        """
        Test get_valid_input with a pattern for phone number validation.
        """
        # Arrange
        prompt = "Enter phone number: "
        error_message = "Invalid phone number."
        pattern = r'^\+?1?\d{9,15}$'
        
        # Act
        result = get_valid_input(str, prompt, error_message, pattern=pattern)
        
        # Assert
        self.assertEqual(result, '+1234567890')  # Check if the result matches the valid phone number

    @patch('builtins.input', side_effect=['invalid-float', '12.34'])
    def test_get_valid_input_float(self, mock_input):
        """
        Test get_valid_input with a valid float input.
        """
        # Arrange
        prompt = "Enter a float number: "
        error_message = "Invalid input."
        pattern = r'^\d+(\.\d{1,2})?$'
        
        # Act
        result = get_valid_input(float, prompt, error_message, pattern=pattern)
        
        # Assert
        self.assertEqual(result, 12.34)  # Check if the result is 12.34

    @patch('builtins.input', side_effect=['invalid-int', '42'])
    def test_get_valid_input_invalid_then_valid_int(self, mock_input):
        """
        Test get_valid_input with an invalid input followed by a valid integer input.
        """
        # Arrange
        prompt = "Enter an integer: "
        error_message = "Invalid input."
        
        # Act
        result = get_valid_input(int, prompt, error_message)
        
        # Assert
        self.assertEqual(result, 42)  # Check if the result is 42

    @patch('builtins.input', side_effect=['123', ''])
    def test_get_valid_input_empty_disallowed(self, mock_input):
        """
        Test get_valid_input with an empty input where empty is not allowed.
        """
        # Arrange
        prompt = "Enter something: "
        error_message = "Invalid input."
        
        # Act
        result = get_valid_input(str, prompt, error_message, allow_empty=False)
        
        # Assert
        self.assertEqual(result, '123')  # Check if the result is '123'

    @patch('builtins.input', side_effect=['abc', 'def'])
    def test_get_valid_input_string(self, mock_input):
        """
        Test get_valid_input with valid string input.
        """
        # Arrange
        prompt = "Enter a string: "
        error_message = "Invalid input."
        
        # Act
        result = get_valid_input(str, prompt, error_message)
        
        # Assert
        self.assertEqual(result, 'abc')  # Check if the result is 'abc'

    @patch('builtins.input', side_effect=['abc'])
    def test_get_valid_input_default_value_without_empty(self, mock_input):
        """
        Test get_valid_input with a default value and empty input not allowed.
        """
        # Arrange
        prompt = "Enter something: "
        error_message = "Invalid input."
        default_value = "default"
        
        # Act
        result = get_valid_input(str, prompt, error_message, default_value=default_value, allow_empty=False)
        
        # Assert
        self.assertEqual(result, 'abc')  # Check if the result is 'abc'

    class TestCafeApp(unittest.TestCase):
        # Existing test cases...

        @patch('builtins.input', side_effect=['', ''])
        def test_update_order_with_empty_courier_input(self, mock_input):
            """
            Test updating an order's courier with empty input.
            """
            # Arrange
            cafe_app_instance = CafeApp()
            cafe_app_instance.courier_list = [{"name": "RoyalMail", "phone": "08007267864"},
                                              {"name": "DPD", "phone": "08431782222"},
                                              {"name": "Evri", "phone": "03303336556"}]
            cafe_app_instance.order_list = [{"customer_name": "John Doe", "customer_address": "123 Main St",
                                              "customer_phone": "+123456789", "courier": "DPD",
                                              "status": "PREPARING", "items": "Coffee"}]

            # Mocking save_data method to avoid actual writing to files
            cafe_app_instance.save_data = lambda: None

            expected_order_courier = "DPD"  # Expected courier remains unchanged

            # Act
            cafe_app_instance.update_order()

            # Assert
            self.assertEqual(cafe_app_instance.order_list[0]["courier"], expected_order_courier)


if __name__ == '__main__':  # Standard boilerplate to run the tests
    unittest.main()  # Run all the tests
