import unittest  # Import the unittest module for creating and running unit tests
import csv  # Import the csv module for reading and writing CSV files
import os  # Import the os module for interacting with the operating system
from src.app import CafeApp  # Import the CafeApp class from the app module

class TestCafeApp(unittest.TestCase):  # Define a test case class that inherits from unittest.TestCase
    def setUp(self):
        """
        This method is called before each test case.
        It sets up the necessary data and environment for the tests.
        """
        self.app = CafeApp()  # Create an instance of the CafeApp class
        self.test_data_dir = os.path.join(os.getcwd(), "test_data")  # Use the current working directory and join "test_data"
        os.makedirs(self.test_data_dir, exist_ok=True)  # Create the test data directory if it doesn't exist
        self.app.data_dir = self.test_data_dir  # Set the data directory for the CafeApp instance
        self.app.products_file = os.path.join(self.test_data_dir, "products.csv")  # Set the file path for products
        self.app.couriers_file = os.path.join(self.test_data_dir, "couriers.csv")  # Set the file path for couriers
        self.app.orders_file = os.path.join(self.test_data_dir, "orders.csv")  # Set the file path for orders
        os.makedirs(self.test_data_dir, exist_ok=True)  # Create the test data directory if it doesn't exist

    def tearDown(self):
        """
        This method is called after each test case.
        It cleans up the test environment by removing the created test data files and directory.
        """
        for file in [self.app.products_file, self.app.couriers_file, self.app.orders_file]:  # Iterate over file paths
            if os.path.exists(file):  # Check if the file exists
                os.remove(file)  # Remove the file
        os.rmdir(self.test_data_dir)  # Remove the test data directory

    def test_load_data(self):
        """
        Test case for the load_data method.
        This test case verifies that the load_data method correctly loads data from the CSV files.
        """
        # Arrange: Create test data files
        with open(self.app.products_file, "w", newline='') as file:  # Open the products file for writing
            writer = csv.writer(file)  # Create a CSV writer object
            writer.writerow(["name", "price"])  # Write the header row
            writer.writerow(["Product 1", "10"])  # Write a data row
            writer.writerow(["Product 2", "20"])  # Write another data row

        # Repeat the same process for couriers and orders files
        with open(self.app.couriers_file, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "phone"])
            writer.writerow(["Courier 1", "123456789"])

        with open(self.app.orders_file, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["customer_name", "customer_address", "customer_phone", "courier", "status", "items"])
            writer.writerow(["John", "123 Main St", "987654321", "1", "PREPARING", "1,2"])

        # Act: Load data
        self.app.load_data()  # Call the load_data method

        # Assert: Check if data is loaded correctly
        self.assertEqual(len(self.app.product_list), 2, "The product_list should have 2 items")  # Assert that the product_list has 2 items
        self.assertEqual(len(self.app.courier_list), 1, "The courier_list should have 1 item")  # Assert that the courier_list has 1 item
        self.assertEqual(len(self.app.order_list), 1, "The order_list should have 1 item")  # Assert that the order_list has 1 item

    def test_save_data(self):
        """
        Test case for the save_data method.
        This test case verifies that the save_data method correctly saves data to the CSV files.
        """
        # Arrange: Add test data to the lists
        self.app.product_list = [{"name": "Product 1", "price": "10"}]
        self.app.courier_list = [{"name": "Courier 1", "phone": "123456789"}]
        self.app.order_list = [{"customer_name": "John", "customer_address": "123 Main St", "customer_phone": "987654321", "courier": "1", "status": "PREPARING", "items": "1"}]

        # Act: Save data
        self.app.save_data()  # Call the save_data method

        # Assert: Check if data is saved correctly
        with open(self.app.products_file, "r") as file:  # Open the products file for reading
            reader = csv.reader(file)  # Create a CSV reader object
            rows = list(reader)  # Read all rows into a list
            self.assertEqual(len(rows), 2, "The products file should have 2 rows (header + data)")  # Assert that there are 2 rows (header + data)
            self.assertEqual(rows[1], ["Product 1", "10"], "The data row in the products file is incorrect")  # Assert that the data row is correct

        # Repeat the same process for couriers and orders files
        with open(self.app.couriers_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 2, "The couriers file should have 2 rows (header + data)")
            self.assertEqual(rows[1], ["Courier 1", "123456789"], "The data row in the couriers file is incorrect")

        with open(self.app.orders_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 2, "The orders file should have 2 rows (header + data)")
            self.assertEqual(rows[1], ["John", "123 Main St", "987654321", "1", "PREPARING", "1"], "The data row in the orders file is incorrect")

if __name__ == "__main__":  # This is a standard Python idiom to run the code when the script is executed directly
    unittest.main()  # Run all the tests




### Data Loading and Saving Functionality Tests:

# Data Loading Test (test_load_data):
# This test evaluates the application's ability to load data from CSV files using the load_data method. It sets up test data files for products, couriers, and orders, writes sample data to these files, 
# and then calls the load_data method to load the data into the respective lists within the CafeApp instance.
# The test then asserts that the loaded data matches the expected values by checking the lengths of the product, courier, and order lists.
# This ensures that the application can successfully read data from CSV files and populate the appropriate data structures.

# Data Saving Test (test_save_data):
# This test verifies the application's capability to save data to CSV files using the save_data method.
# It first arranges test data by manually setting the product, courier, and order lists within the CafeApp instance.
# Then, it calls the save_data method to write this test data to CSV files.
# Afterward, the test reads the CSV files and compares the content with the expected values to ensure that the data was correctly written.
# This test guarantees that the application can effectively store data in CSV format for future use or retrieval.

# Test Setup (setUp Method):
# - This method is executed before each test case to prepare the test environment.
# - It creates an instance of the CafeApp class and sets up the necessary directories and file paths for test data.
# - Additionally, it creates the test data directory if it doesn't exist already.

# Test Teardown (tearDown Method):
# - This method is called after each test case to clean up the test environment.
# - It removes the test data files and directory created during the test setup phase to ensure that subsequent tests start with a clean slate.
# - This prevents interference between different test cases and maintains the integrity of the testing process.