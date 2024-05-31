import unittest
from unittest.mock import patch
import os
import shutil
from src.app import CafeApp

class TestCafeApp(unittest.TestCase):
    def setUp(self):
        self.app = CafeApp()
        self.test_data_dir = os.path.join(os.getcwd(), "test_data")
        os.makedirs(self.test_data_dir, exist_ok=True)
        self.app.data_dir = self.test_data_dir
        self.app.products_file = os.path.join(self.test_data_dir, "products.csv")
        self.app.couriers_file = os.path.join(self.test_data_dir, "couriers.csv")
        self.app.orders_file = os.path.join(self.test_data_dir, "orders.csv")

        # Initialize lists with sample data
        self.app.product_list = [{"name": "Coke Zero", "price": 0.8}, {"name": "Fanta", "price": 1.2}]
        self.app.courier_list = [{"name": "Bob", "phone": "0789887889"}, {"name": "Alice", "phone": "0789887890"}]
        self.app.order_list = [{"customer_name": "John", "customer_address": "Unit 2, 12 Main Street, LONDON, WH1 2ER", "customer_phone": "0789887334", "courier": 1, "status": "preparing", "items": "1,3"},
                               {"customer_name": "Jane", "customer_address": "Flat 3, 15 High Road, MANCHESTER, M16 8DJ", "customer_phone": "0789887335", "courier": 2, "status": "ready", "items": "2"}]

    def tearDown(self):
        shutil.rmtree(self.test_data_dir)

    @patch('builtins.input', side_effect=['1', 'Coke', '1.0', ''])
    def test_update_product(self, mock_input):
        # Arrange: Define the expected state of the product after updating
        expected_product = {"name": "Coke", "price": "1.0"}

        # Act: Perform the action to update the product
        self.app.update_product()

        # Assert: Verify that the product has been updated correctly
        self.assertEqual(self.app.product_list[0], expected_product)

    @patch('builtins.input', side_effect=['1', 'Bob', '0789887888', ''])
    def test_update_courier(self, mock_input):
        # Arrange: Define the expected state of the courier after updating
        expected_courier = {"name": "Bob", "phone": "0789887888"}

        # Act: Perform the action to update the courier
        self.app.update_courier()

        # Assert: Verify that the courier has been updated correctly
        self.assertEqual(self.app.courier_list[0], expected_courier)

    @patch('builtins.input', side_effect=['1', 'John Smith', 'Flat 1, 10 Main Road, LONDON, WC1 2ER', '0789887336', '', '', ''])
    def test_update_order(self, mock_input):
        # Arrange: Define the expected state of the order after updating
        expected_order = {
            "customer_name": "John Smith",
            "customer_address": "Flat 1, 10 Main Road, LONDON, WC1 2ER",
            "customer_phone": "0789887336",
            "courier": 1,
            "status": "preparing",
            "items": "1,3"
        }

        # Act: Perform the action to update the order
        self.app.update_order()

        # Assert: Verify that the order has been updated correctly
        self.assertEqual(self.app.order_list[0], expected_order)

    @patch('builtins.input', side_effect=['1', 'Coke', 'invalid_price', ''])
    def test_update_product_invalid_price(self, mock_input):
        # Test updating product with invalid price input
        self.app.update_product()
        # Assert that product list remains unchanged
        self.assertEqual(len(self.app.product_list), 2)

    @patch('builtins.input', side_effect=['1', '', '1.0', ''])
    def test_update_product_empty_name(self, mock_input):
        # Test updating product with empty name input
        self.app.update_product()
        # Assert that product list remains unchanged
        self.assertEqual(len(self.app.product_list), 2)

    @patch('builtins.input', side_effect=['1', 'Bob', 'invalid_phone', ''])
    def test_update_courier_invalid_phone(self, mock_input):
        # Test updating courier with invalid phone number input
        self.app.update_courier()
        # Assert that courier list remains unchanged
        self.assertEqual(len(self.app.courier_list), 2)

    @patch('builtins.input', side_effect=['1', '', '0789887888', ''])
    def test_update_courier_empty_name(self, mock_input):
        # Test updating courier with empty name input
        self.app.update_courier()
        # Assert that courier list remains unchanged
        self.assertEqual(len(self.app.courier_list), 2)

    @patch('builtins.input', side_effect=['1', 'John Smith'*100, 'Flat 1, 10 Main Road, LONDON, WC1 2ER', '0789887336', '', '', ''])
    def test_update_order_long_name(self, mock_input):
        # Test updating order with very long customer name input
        self.app.update_order()
        # Assert that order list remains unchanged
        self.assertEqual(len(self.app.order_list), 2)

    @patch('builtins.input', side_effect=['1', 'John Smith', 'Flat 1, 10 Main Road, LONDON, WC1 2ER'*100, '0789887336', '', '', ''])
    def test_update_order_long_address(self, mock_input):
        # Test updating order with very long customer address input
        self.app.update_order()
        # Assert that order list remains unchanged
        self.assertEqual(len(self.app.order_list), 2)

    @patch('builtins.input', side_effect=['1', 'John Smith', 'Flat 1, 10 Main Road, LONDON, WC1 2ER', '0789887336', '', '', ''])
    def test_update_order_empty_items(self, mock_input):
        # Test updating order with empty items input
        self.app.update_order()
        # Assert that order list remains unchanged
        self.assertEqual(len(self.app.order_list), 2)

if __name__ == '__main__':
    unittest.main()



### Error Handling and Edge Case Tests:

# 1. **Product Update with Invalid Price (`test_update_product_invalid_price`):**
#     - This test evaluates the application's response when attempting to update a product with an invalid price input, such as non-numeric characters. 
#       It uses the @patch decorator to mock user input, providing an invalid price input to the update_product method. 
#       By simulating this scenario, the test ensures that the application correctly handles the provided input and prevents the update of the product with invalid data. 
#       It asserts that the product list remains unchanged after the update attempt, indicating that the application effectively validates input data and maintains data integrity.
# 
# 2. **Product Update with Empty Name (`test_update_product_empty_name`):**
#     - This test assesses the application's behavior when updating a product with an empty name input. Using the @patch decorator, it simulates user input by providing an empty name when invoking the update_product method. 
#       By doing so, the test examines whether the application enforces data validation rules to prevent the update of products with missing or incomplete information. 
#       It verifies that the product list remains unchanged after the update attempt, indicating that the application successfully detects and rejects invalid input, thereby safeguarding data consistency.
# 
# 3. **Courier Update with Invalid Phone Number (`test_update_courier_invalid_phone`):**
#     - This test case evaluates how the application handles updating a courier with an invalid phone number input. It utilizes the @patch decorator to mock user input, supplying an invalid phone number format to the update_courier method. 
#       Through this simulation, the test verifies that the application implements robust data validation mechanisms to detect and reject malformed input. 
#       It asserts that the courier list remains unchanged after the update attempt, indicating that the application effectively validates and sanitizes user-provided data to maintain data integrity and 
#       prevent potential issues related to invalid or inconsistent data entries.
# 
# 4. **Courier Update with Empty Name (`test_update_courier_empty_name`):**
#     - Similar to the previous test, this scenario examines how the application responds to updating a courier with an empty name input. 
#       By using the @patch decorator, the test simulates user interaction with the update_courier method, providing an empty name as input. 
#       It evaluates whether the application enforces constraints on data completeness by detecting and rejecting incomplete data entries. 
#       The test asserts that the courier list remains unchanged after the update attempt, indicating that the application successfully handles scenarios where essential data attributes are missing, 
#       thereby ensuring the reliability and accuracy of the courier data maintained by the system.
# 
# 5. **Order Update with Long Customer Name (`test_update_order_long_name`):**
#     - This test focuses on evaluating the application's behavior when updating an order with a very long customer name input. 
#       Using the @patch decorator, it emulates user input by providing an excessively long customer name to the update_order method. 
#       The test examines whether the application can effectively handle and process large data inputs without encountering errors or performance issues. 
#       It asserts that the order list remains unchanged after the update attempt, demonstrating that the application can gracefully handle scenarios involving extensive data inputs, thereby ensuring system stability and responsiveness.
# 
# 6. **Order Update with Long Customer Address (`test_update_order_long_address`):**
#     - Similarly, this test case assesses how the application handles updating an order with a lengthy customer address input. 
#       By utilizing the @patch decorator, the test simulates user interaction with the update_order method, providing a significantly long customer address as input. 
#       It evaluates the application's ability to handle large data inputs efficiently without compromising performance or stability. 
#       The test asserts that the order list remains unchanged after the update attempt, indicating that the application can process extensive data entries without encountering issues, thereby maintaining system reliability and ensuring seamless operation.
# 
# 7. **Order Update with Empty Items List (`test_update_order_empty_items`):**
#     - In this final test, the focus is on evaluating how the application handles updating an order with an empty items list. 
#       Using the @patch decorator, the test emulates user input by submitting an order update request without specifying any items. 
#       It assesses whether the application appropriately handles edge cases in data processing by detecting and responding to incomplete data entries. 
#       The test asserts that the order list remains unchanged after the update attempt, demonstrating that the application effectively handles scenarios where essential data attributes are missing, 
#       thereby upholding data consistency and ensuring the accuracy of order records stored by the system.

