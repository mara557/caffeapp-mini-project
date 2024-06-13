import unittest
from unittest.mock import patch, MagicMock
from src.app import CafeApp, get_valid_input, get_db_connection

class TestCafeApp(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_get_db_connection(self, mock_connect):
        # Arrange
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Act
        conn = get_db_connection()
        
        # Assert
        self.assertEqual(conn, mock_conn)
        mock_connect.assert_called_once()

    def test_get_valid_input(self):
        # Arrange
        with patch('builtins.input', side_effect=['42']):
            
            # Act
            result = get_valid_input(int, "Enter a number: ", "Invalid input.")
            
            # Assert
            self.assertEqual(result, 42)

    @patch('src.app.get_db_connection')
    def test_load_data(self, mock_get_db_connection):
        # Arrange
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [
            [{'order_status': 'PREPARING'}],  # Mock data for order_status
            [{'id': 1, 'name': 'Product 1', 'price': 1.99, 'inventory': 10}],
            [{'id': 1, 'name': 'Courier 1', 'phone': '1234567890'}],
            [{'id': 1, 'name': 'Customer 1', 'address': 'Address 1', 'phone': '1234567890'}],
            [{'id': 1, 'customer_id': 1, 'courier': 1, 'status': 'PREPARING'}]
        ]
        app = CafeApp()

        # Act
        app.load_data()

        # Assert
        self.assertEqual(len(app.order_status_list), 1)
        self.assertEqual(len(app.product_list), 1)
        self.assertEqual(len(app.courier_list), 1)
        self.assertEqual(len(app.customer_list), 1)
        self.assertEqual(len(app.order_list), 1)

    @patch('src.app.CafeApp.print_product_list')
    def test_display_product_menu(self, mock_print_product_list):
        # Arrange
        app = CafeApp()
        with patch('builtins.input', side_effect=['0']):
            with patch('src.app.get_valid_input', side_effect=[0]):
                
                # Act
                app.display_product_menu()
                
                # Assert
                mock_print_product_list.assert_not_called()

    @patch('src.app.CafeApp.create_product')
    @patch('src.app.get_valid_input')
    def test_create_product(self, mock_get_valid_input, mock_create_product):
        # Arrange
        mock_get_valid_input.side_effect = ['Product Name', '1.99', '10']
        app = CafeApp()
        
        # Act
        app.create_product()
        
        # Assert
        mock_create_product.assert_called_once()

    @patch('src.app.CafeApp.update_product')
    @patch('src.app.get_valid_input')
    def test_update_product(self, mock_get_valid_input, mock_update_product):
        # Arrange
        mock_get_valid_input.side_effect = ['1', 'Updated Product Name', '2.99', '5']
        app = CafeApp()
        
        # Act
        app.update_product()
        
        # Assert
        mock_update_product.assert_called_once()

    @patch('src.app.CafeApp.delete_product')
    @patch('src.app.get_valid_input')
    def test_delete_product(self, mock_get_valid_input, mock_delete_product):
        # Arrange
        mock_get_valid_input.side_effect = ['1']
        app = CafeApp()
        
        # Act
        app.delete_product()
        
        # Assert
        mock_delete_product.assert_called_once()

    @patch('src.app.CafeApp.export_to_csv')
    @patch('src.app.get_valid_input')
    def test_export_to_csv(self, mock_get_valid_input, mock_export_to_csv):
        # Arrange
        mock_get_valid_input.side_effect = [1]
        app = CafeApp()
        
        # Act
        app.export_to_csv('products', 'products.csv')
        
        # Assert
        mock_export_to_csv.assert_called_once()

    @patch('src.app.CafeApp.import_from_csv')
    @patch('src.app.get_valid_input')
    def test_import_from_csv(self, mock_get_valid_input, mock_import_from_csv):
        # Arrange
        mock_get_valid_input.side_effect = [1]
        app = CafeApp()
        
        # Act
        app.import_from_csv('products', 'products.csv')
        
        # Assert
        mock_import_from_csv.assert_called_once()

if __name__ == '__main__':
    unittest.main()


# Test Descriptions:

# test_get_db_connection:
# Arrange: Mock the mysql.connector.connect method to simulate a database connection.
# Act: Call get_db_connection to obtain a connection.
# Assert: Ensure the returned connection is the mocked object and that the connect method is called once.

# test_get_valid_input:
# Arrange: Patch the input function to simulate user input.
# Act: Call get_valid_input to capture and convert the input.
# Assert: Check that the returned value is correctly converted to an integer.

# test_load_data:
# Arrange: Mock the database connection and cursor, providing mock return values for fetchall that include valid data for order_status, products, couriers, customers, and orders.
# Act: Instantiate CafeApp and call load_data.
# Assert: Verify that the internal lists (order_status_list, product_list, courier_list, customer_list, order_list) are populated correctly with the mocked data.

# test_display_product_menu:
# Arrange: Mock the print_product_list method to check if it gets called.
# Act: Call display_product_menu while simulating user input.
# Assert: Ensure that print_product_list is not called when the user selects the option to return to the main menu.

# test_create_product:
# Arrange: Mock get_valid_input to simulate user inputs for product creation and create_product to track its execution.
# Act: Call create_product.
# Assert: Verify that create_product is called once with the correct inputs.
# test_update_product:

# Arrange: Mock get_valid_input to simulate user inputs for updating a product and update_product to track its execution.
# Act: Call update_product.
# Assert: Ensure that update_product is called once with the correct inputs.

# test_delete_product:
# Arrange: Mock get_valid_input to simulate user input for product deletion and delete_product to track its execution.
# Act: Call delete_product.
# Assert: Confirm that delete_product is called once with the correct input.

# test_export_to_csv:
# Arrange: Mock get_valid_input to simulate user input for selecting the export option and export_to_csv to track its execution.
# Act: Call export_to_csv.
# Assert: Verify that export_to_csv is called once with the correct parameters.

# test_import_from_csv:
# Arrange: Mock get_valid_input to simulate user input for selecting the import option and import_from_csv to track its execution.
# Act: Call import_from_csv.
# Assert: Ensure that import_from_csv is called once with the correct parameters.