import unittest
from unittest.mock import patch
import csv
import os
import shutil
from src.app import CafeApp

class TestCafeAppCreate(unittest.TestCase):
    def setUp(self):
        self.app = CafeApp()
        self.test_data_dir = os.path.join(os.getcwd(), "test_data")
        os.makedirs(self.test_data_dir, exist_ok=True)
        self.app.data_dir = self.test_data_dir
        self.app.products_file = os.path.join(self.test_data_dir, "products.csv")
        self.app.couriers_file = os.path.join(self.test_data_dir, "couriers.csv")
        self.app.orders_file = os.path.join(self.test_data_dir, "orders.csv")

    def tearDown(self):
        shutil.rmtree(self.test_data_dir)

    @patch('builtins.input', side_effect=["New Product", "15.99", "John Doe", "1234567890", "Jane Smith", "123 Main St", "5678901234", "1", "1"])
    def test_create_methods(self, mock_input):
        """
        Test case for the create_product, create_courier, and create_order methods.

        This test case verifies that the create methods correctly create new products, couriers, and orders.
        It mocks the user input with side_effect to simulate user input for creating a new product, courier, and order.
        """
        # Arrange: Define the expected outputs
        expected_product_output = {"name": "New Product", "price": 15.99}
        expected_courier_output = [{"name": "John Doe", "phone": "1234567890"}]
        expected_order_output = [{"customer_name": "Jane Smith", "customer_address": "123 Main St", "customer_phone": "5678901234", "courier": "1", "status": "PREPARING", "items": "1"}]

        # Act: Call the create methods
        self.app.create_product()
        self.app.create_courier()
        self.app.create_order()

        # Assert: Verify the product creation
        self.assertIn(expected_product_output, self.app.product_list, "The new product should be added to the product_list")
        with open(self.app.products_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(rows[-1], ["New Product", "15.99"], "The new product should be saved to the products file")

        # Assert: Verify the courier creation
        self.assertEqual(self.app.courier_list, expected_courier_output, "The new courier should be added to the courier_list")

        # Assert: Verify the order creation
        self.assertEqual(self.app.order_list, expected_order_output, "The new order should be added to the order_list")

if __name__ == "__main__":
    unittest.main()






# Test Cases for Create Methods:
# Test Case for Creating Products, Couriers, and Orders (test_create_methods):
# This test case evaluates the create_product, create_courier, and create_order methods of the CafeApp class.
# It mocks user input using the side_effect parameter to simulate user interaction for creating a new product, courier, and order.
# The test arranges the expected outputs for the new product, courier, and order.
# Then, it calls the create methods and asserts that the new items are correctly added to their respective lists (product_list, courier_list, order_list) within the CafeApp instance.
# Additionally, it checks if the new product is correctly saved to the products file by reading the CSV file.
# This test ensures that the application can accurately create and store new products, couriers, and orders based on user input.

# Test Setup and Teardown
# Test Setup (setUp Method):
# - This method is executed before each test case to set up the necessary data and environment.
# - It creates an instance of the CafeApp class and sets up the directories and file paths for test data.
# - Additionally, it creates the test data directory if it doesn't exist already.
# 
# Test Teardown (tearDown Method):
# - This method is called after each test case to clean up the test environment.
# - It removes the test data files and directory created during the test setup phase to ensure a clean slate for subsequent tests.
# - This prevents interference between different test cases and maintains the integrity of the testing process.