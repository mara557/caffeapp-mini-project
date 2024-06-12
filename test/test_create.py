import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from src.app import CafeApp

class TestCafeApp(unittest.TestCase):
    
    def setUp(self):
        self.app = CafeApp()
        self.app.db_conn = MagicMock()

    @patch('builtins.input', side_effect=['Test Product', '10.50', '50'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_create_product(self, mock_stdout, mock_input):
        # Arrange
        cursor_mock = MagicMock()
        self.app.db_conn.cursor.return_value = cursor_mock
        cursor_mock.lastrowid = 1

        # Act
        self.app.create_product()

        # Assert
        cursor_mock.execute.assert_any_call("INSERT INTO products (name, price, inventory) VALUES (%s, %s, %s)", ('Test Product', 10.50, 50))
        self.app.db_conn.commit.assert_called_once()
        self.assertIn("Product added successfully!", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['Test Courier', '+1234567890'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_create_courier(self, mock_stdout, mock_input):
        # Arrange
        cursor_mock = MagicMock()
        self.app.db_conn.cursor.return_value = cursor_mock
        cursor_mock.lastrowid = 1

        # Act
        self.app.create_courier()

        # Assert
        cursor_mock.execute.assert_any_call("INSERT INTO couriers (name, phone) VALUES (%s, %s)", ('Test Courier', '+1234567890'))
        self.app.db_conn.commit.assert_called_once()
        self.assertIn("Courier added successfully!", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['Test Customer', 'Test Address', '+1234567890'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_create_customer(self, mock_stdout, mock_input):
        # Arrange
        cursor_mock = MagicMock()
        self.app.db_conn.cursor.return_value = cursor_mock
        cursor_mock.lastrowid = 1

        # Act
        self.app.create_customer()

        # Assert
        cursor_mock.execute.assert_any_call("INSERT INTO customers (name, address, phone) VALUES (%s, %s, %s)", ('Test Customer', 'Test Address', '+1234567890'))
        self.app.db_conn.commit.assert_called_once()
        self.assertIn("Customer added successfully!", mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()




#  Structure
#  Imports:
#  unittest, patch, MagicMock, StringIO, and CafeApp.
#  
#  TestCafeApp Class:
#  setUp: Initializes CafeApp instance and mocks the database connection.
#  
#  test_create_product:
#  Mocks input and sys.stdout.
#  Uses cursor_mock to simulate database cursor.
#  Verifies SQL query execution, database commit, and success message.
#  
#  test_create_courier:
#  Similar to test_create_product.
#  Verifies correct SQL query, database commit, and success message.
#  
#  test_create_customer:
#  Similar to test_create_product.
#  Verifies correct SQL query, database commit, and success message.
#  
#  Key Components
#  Mocking User Input: @patch('builtins.input', side_effect=['...']) simulates user input.
#  Mocking Print Statements: @patch('sys.stdout', new_callable=StringIO) captures console output.
#  Mocking Database: MagicMock mocks database connection and cursor.
#  Verifying SQL Execution: cursor_mock.execute.assert_any_call("SQL QUERY", PARAMETERS) checks SQL query execution.
#  Verifying Commit Call: self.app.db_conn.commit.assert_called_once() ensures the commit is called once.
#  Verifying Output: self.assertIn("MESSAGE", mock_stdout.getvalue()) checks printed messages.