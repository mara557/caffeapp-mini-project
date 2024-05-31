import unittest
from unittest.mock import patch
import os
import shutil
from src.app import CafeApp

class TestCafeAppDelete(unittest.TestCase):
    def setUp(self):
        self.app = CafeApp()
        self.test_data_dir = os.path.join(os.getcwd(), "test_data")
        os.makedirs(self.test_data_dir, exist_ok=True)
        self.app.data_dir = self.test_data_dir
        self.app.products_file = os.path.join(self.test_data_dir, "products.csv")
        self.app.couriers_file = os.path.join(self.test_data_dir, "couriers.csv")
        self.app.orders_file = os.path.join(self.test_data_dir, "orders.csv")

        # Initialize lists with sample data
        self.app.product_list = [{"name": "Product 1", "price": "10.00"}, {"name": "Product 2", "price": "15.99"}]
        self.app.courier_list = [{"name": "John Doe", "phone": "1234567890"}, {"name": "Jane Smith", "phone": "0987654321"}]
        self.app.order_list = [{"customer_name": "John Doe", "customer_address": "123 Main St", "customer_phone": "1234567890", "courier": "1", "status": "PREPARING", "items": "1"},
                               {"customer_name": "Jane Smith", "customer_address": "456 Oak Rd", "customer_phone": "5678901234", "courier": "2", "status": "READY", "items": "2"}]

    def tearDown(self):
        shutil.rmtree(self.test_data_dir)
        
    @patch('builtins.input', side_effect=["1", "1", "1"])
    def test_delete_methods(self, mock_input):
        """
        Test case for the delete_product, delete_courier, and delete_order methods.

        This test case verifies that the delete methods correctly remove the selected items from the respective lists.
        It mocks the user input with side_effect to simulate selecting the first item in each list for deletion.
        """
        # Arrange: Define the expected outputs
        expected_product_output = [{"name": "Product 2", "price": "15.99"}]
        expected_courier_output = [{"name": "Jane Smith", "phone": "0987654321"}]
        expected_order_output = [{"customer_name": "Jane Smith", "customer_address": "456 Oak Rd", "customer_phone": "5678901234", "courier": "2", "status": "READY", "items": "2"}]

        # Act: Call the delete methods
        self.app.delete_product()
        self.app.delete_courier()
        self.app.delete_order()

        # Assert: Verify the product deletion
        self.assertEqual(self.app.product_list, expected_product_output, "The first product should be deleted from the product_list")

        # Assert: Verify the courier deletion
        self.assertEqual(self.app.courier_list, expected_courier_output, "The first courier should be deleted from the courier_list")

        # Assert: Verify the order deletion
        self.assertEqual(self.app.order_list, expected_order_output, "The first order should be deleted from the order_list")

    @patch('builtins.input', side_effect=["999", "999", "999"])
    def test_delete_invalid_index(self, mock_input):
        """
        Test case to verify the behavior of the delete methods when an invalid index is provided.

        This test case verifies that the delete methods do not modify the respective lists when an invalid index is provided.
        It mocks the user input with side_effect to simulate providing an invalid index (999) for each list.
        """
        # Arrange: Define the initial lists
        initial_product_list = self.app.product_list.copy()
        initial_courier_list = self.app.courier_list.copy()
        initial_order_list = self.app.order_list.copy()

        # Act: Call the delete methods with invalid indexes
        self.app.delete_product()
        self.app.delete_courier()
        self.app.delete_order()

        # Assert: Verify that the lists remain unchanged
        self.assertEqual(self.app.product_list, initial_product_list, "The product_list should remain unchanged")
        self.assertEqual(self.app.courier_list, initial_courier_list, "The courier_list should remain unchanged")
        self.assertEqual(self.app.order_list, initial_order_list, "The order_list should remain unchanged")

if __name__ == "__main__":
    unittest.main()





# Test Cases for Delete Methods
# Test Case for Deleting Products, Couriers, and Orders (test_delete_methods):
# This test case evaluates the delete_product, delete_courier, and delete_order methods of the CafeApp class.
# It mocks user input using the side_effect parameter to simulate selecting the first item in each list for deletion.
# The test arranges the expected outputs after deletion.
# Then, it calls the delete methods and asserts that the selected items are correctly removed from their respective lists (product_list, courier_list, order_list) within the CafeApp instance.
# This test ensures that the application can accurately delete products, couriers, and orders based on user input.

# Test Case for Handling Invalid Index (test_delete_invalid_index):
# This test case verifies the behavior of the delete methods when an invalid index is provided.
# It mocks user input with side_effect to simulate providing an invalid index (999) for each list.
# The test arranges the initial lists before deletion.
# Then, it calls the delete methods with invalid indexes.
# Finally, it asserts that the lists remain unchanged after attempting deletion with invalid indexes.
# This test guarantees that the application handles invalid input gracefully without modifying the lists unexpectedly.

# Test Setup (setUp Method):
# This method is executed before each test case to set up the necessary data for the tests. It initializes the CafeApp instance with predefined product, courier, and order lists.

# Test Teardown (tearDown Method):
# Since there's no specific teardown required for these tests, the default teardown provided by the unittest framework will be used, which doesn't need to be explicitly defined.    