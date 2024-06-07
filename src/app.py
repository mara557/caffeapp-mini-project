import mysql.connector
import os
import re
import csv
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    conn.autocommit = True
    return conn

def get_valid_input(input_type, prompt, error_message, pattern=None, default_value=None, allow_empty=False):
    while True:
        value = input(prompt)

        # Check for empty input
        if not value:
            if allow_empty:
                return default_value if default_value is not None else ""
            else:
                print(f"\033[91m{error_message}\033[0m")
                continue

        # Check for pattern match (if provided)
        if pattern:
            if re.match(pattern, value):
                try:
                    return input_type(value)
                except ValueError:
                    print(f"\033[91m{error_message}\033[0m")
                    continue
            else:
                print(f"\033[91m{error_message}\033[0m")
                continue

        # If no pattern is provided, just try to convert to the desired input_type
        try:
            return input_type(value)
        except ValueError:
            print(f"\033[91m{error_message}\033[0m")
            continue

class CafeApp:
    
    def __init__(self):
        self.db_conn = get_db_connection()
        self.order_list = []
        self.order_status_list = self.load_order_statuses()

    def load_order_statuses(self):
        cursor = self.db_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM order_status")
        statuses = cursor.fetchall()
        cursor.close()
        return [status['order_status'] for status in statuses]

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_data(self):
        cursor = self.db_conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM products")
        self.product_list = cursor.fetchall()
        
        cursor.execute("SELECT * FROM couriers")
        self.courier_list = cursor.fetchall()
        
        cursor.execute("SELECT * FROM customers")
        self.customer_list = cursor.fetchall()
        
        cursor.execute("SELECT * FROM orders")
        self.order_list = cursor.fetchall()
        
        cursor.close()

    
    
    def display_main_menu(self):
        self.clear_screen()
        main_menu = (f"\033[38;2;226;135;67mMain Menu\033[0m"
                     "\n 0. Exit application"
                     "\n 1. Product Menu"
                     "\n 2. Courier Menu"
                     "\n 3. Customer Menu"
                     "\n 4. Orders Menu"
                     "\n 5. Data Import/Export Menu")
        print(main_menu)

    def display_product_menu(self):
        product_menu = (f"\033[38;2;226;135;67mProduct Menu\033[0m"
                        "\n 0 - Return to Main Menu"
                        "\n 1 - Print Products List"
                        "\n 2 - Create New Product"
                        "\n 3 - Update Existing Product"
                        "\n 4 - Delete Product")
        print(product_menu)

    def display_courier_menu(self):
        courier_menu = (f"\033[38;2;226;135;67mCourier Menu\033[0m"
                        "\n 0 - Return to Main Menu"
                        "\n 1 - Print Couriers List"
                        "\n 2 - Create New Courier"
                        "\n 3 - Update Existing Courier"
                        "\n 4 - Delete Courier")
        print(courier_menu)

    def display_customer_menu(self):
        customer_menu = (f"\033[38;2;226;135;67mCustomer Menu\033[0m"
                         "\n 0 - Return to Main Menu"
                         "\n 1 - Print Customer List"
                         "\n 2 - Create New Customer"
                         "\n 3 - Update Existing Customer"
                         "\n 4 - Delete Customer")
        print(customer_menu)

    def display_order_menu(self):
        order_menu = (f"\033[38;2;226;135;67mOrder Menu\033[0m"
                      "\n 0 - Return to Main Menu"
                      "\n 1 - Print Order List"
                      "\n 2 - Create Order"
                      "\n 3 - Update Existing Order Status"
                      "\n 4 - Update Existing Order"
                      "\n 5 - Delete Order")
        print(order_menu)
    
    def display_data_import_export_menu(self):
        data_import_export_menu = (f"\033[38;2;226;135;67mData Import/Export Menu\033[0m"
                                   "\n 0. Return to Main Menu"
                                   "\n 1. Export Data"
                                   "\n 2. Import Data")
        print(data_import_export_menu)
    
    def display_export_menu(self):
        export_menu = (f"\033[38;2;226;135;67mExport Data Menu\033[0m"
                       "\n 0. Return to Import/Export Menu"
                       "\n 1. Export Products to CSV"
                       "\n 2. Export Couriers to CSV"
                       "\n 3. Export Customers to CSV"
                       "\n 4. Export Orders to CSV")
        print(export_menu)

    def display_import_menu(self):
        import_menu = (f"\033[38;2;226;135;67mImport Data Menu\033[0m"
                       "\n 0. Return to Import/Export Menu"
                       "\n 1. Import Products from CSV"
                       "\n 2. Import Couriers from CSV"
                       "\n 3. Import Customers from CSV"
                       "\n 4. Import Orders from CSV")
        print(import_menu)


    
    def print_product_list(self):
        self.load_data()
        print("\033[93mProduct List:\033[0m")
        if not self.product_list:
            print("\033[90mEmpty\033[0m")
        else:
            max_name_length = max(len(product['name']) for product in self.product_list)
            max_index_length = len(str(len(self.product_list)))
            for i, product in enumerate(self.product_list, start=1):
                index_str = str(i).rjust(max_index_length)
                name = product['name'].ljust(max_name_length)
                print(f"{index_str}. {name}     £{product['price']}     Inventory: {product['inventory']}")

    def create_product(self):
        name = get_valid_input(str, "Enter product name: ", "Invalid input. Please enter a valid name.")
        price = get_valid_input(float, "Enter product price: ", "Invalid input. Please enter a valid price.", pattern=r'^\d+(\.\d{1,2})?$')
        inventory = get_valid_input(int, "Enter product inventory: ", "Invalid input. Please enter a valid inventory.")

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("START TRANSACTION")
            cursor.execute("INSERT INTO products (name, price, inventory) VALUES (%s, %s, %s)", (name, price, inventory))
            self.db_conn.commit()
            cursor.close()
            print("\033[92mProduct added successfully!\033[0m")
        except mysql.connector.Error as err:
            self.db_conn.rollback()
            print(f"\033[91mFailed to add product: {err}\033[0m")

    def update_product(self):
        self.print_product_list()
        index = get_valid_input(int, "Enter the index of the product to update: ", "Invalid input. Please enter a valid index.") - 1

        if 0 <= index < len(self.product_list):
            product = self.product_list[index]
            product_id = product['id']
            updates = {}

            # Collect updates
            for key in ['name', 'price', 'inventory']:
                value = input(f"Enter new {key} (Leave blank to keep: {product[key]}): ")
                if value:
                    updates[key] = value

            # Check if there are any updates
            if updates:
                try:
                    cursor = self.db_conn.cursor()
                    cursor.execute("START TRANSACTION")
                    # Create update query dynamically
                    update_query = ", ".join([f"{k} = %s" for k in updates.keys()])
                    cursor.execute(f"UPDATE products SET {update_query} WHERE id = %s", (*updates.values(), product_id))
                    self.db_conn.commit()
                    cursor.close()
                    self.clear_screen()
                    print("\033[92mProduct updated successfully!\033[0m")
                    self.load_data()
                except mysql.connector.Error as err:
                    self.db_conn.rollback()
                    print(f"\033[91mFailed to update product: {err}\033[0m")
            else:
                self.clear_screen()
                print("\033[93mNo changes made.\033[0m")
        else:
            print("\033[91mInvalid product index.\033[0m")

    def delete_product(self):
        self.print_product_list()
        index = get_valid_input(int, "Enter the index of the product to delete: ", "Invalid input. Please enter a valid index.") - 1

        if 0 <= index < len(self.product_list):
            product = self.product_list[index]
            product_id = product['id']

            confirmation = get_valid_input(str, f"Are you sure you want to delete the product '{product['name']}'? (y/n): ", "Invalid input. Please enter 'y' or 'n'.", pattern=r'^(y|n)$')
            if confirmation.lower() == 'y':
                try:
                    cursor = self.db_conn.cursor()
                    cursor.execute("START TRANSACTION")

                    # Check for orders containing this product
                    cursor.execute("SELECT order_id FROM order_items WHERE product_id = %s", (product_id,))
                    orders = cursor.fetchall()
                    
                    # Delete associated order items and orders if necessary
                    if orders:
                        for order in orders:
                            cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order['order_id'],))
                            cursor.execute("DELETE FROM orders WHERE id = %s", (order['order_id'],))
                    
                    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
                    self.db_conn.commit()
                    cursor.close()
                    print("\033[92mProduct and associated orders deleted successfully!\033[0m")
                    self.load_data()
                except mysql.connector.Error as err:
                    self.db_conn.rollback()
                    print(f"\033[91mFailed to delete product: {err}\033[0m")
            else:
                print("\033[93mProduct deletion cancelled.\033[0m")
        else:
            print("\033[91mInvalid product index.\033[0m")


    
    def print_courier_list(self):
        self.load_data()  # Ensure data is loaded before printing
        print("\033[93mCourier List:\033[0m")
        if not self.courier_list:
            print("\033[90mEmpty\033[0m")
        else:
            max_name_length = max(len(courier['name']) for courier in self.courier_list)
            max_phone_length = max(len(courier['phone']) for courier in self.courier_list)
            max_index_length = len(str(len(self.courier_list)))
            for i, courier in enumerate(self.courier_list, start=1):
                index_str = str(i).rjust(max_index_length)
                name = courier['name'].ljust(max_name_length)
                phone = courier['phone'].ljust(max_phone_length)
                print(f"{index_str}. {name}  {phone}")

    def create_courier(self):
        name = get_valid_input(str, "Enter courier name: ", "Invalid input. Please enter a valid name.")
        phone = get_valid_input(str, "Enter courier phone number: ", "Invalid input. Please enter a valid phone number.", pattern=r'^\+?1?\d{9,15}$')

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("START TRANSACTION")
            cursor.execute("INSERT INTO couriers (name, phone) VALUES (%s, %s)", (name, phone))
            self.db_conn.commit()
            cursor.close()
            print("\033[92mCourier added successfully!\033[0m")
            self.load_data()
        except mysql.connector.Error as err:
            self.db_conn.rollback()
            print(f"\033[91mFailed to add courier: {err}\033[0m")

    def update_courier(self):
        self.print_courier_list()
        index = get_valid_input(int, "Enter the index of the courier to update: ", "Invalid input. Please enter a valid index.") - 1

        if 0 <= index < len(self.courier_list):
            courier = self.courier_list[index]
            courier_id = courier['id']
            updates = {}

            # Collect updates
            for key in ['name', 'phone']:
                value = input(f"Enter new {key} (Leave blank to keep: {courier[key]}): ")
                if value:
                    updates[key] = value

            # Check if there are any updates
            if updates:
                try:
                    cursor = self.db_conn.cursor()
                    cursor.execute("START TRANSACTION")
                    # Create update query dynamically
                    update_query = ", ".join([f"{k} = %s" for k in updates.keys()])
                    cursor.execute(f"UPDATE couriers SET {update_query} WHERE id = %s", (*updates.values(), courier_id))
                    self.db_conn.commit()
                    cursor.close()
                    self.clear_screen()
                    print("\033[92mCourier updated successfully!\033[0m")
                    self.load_data()
                except mysql.connector.Error as err:
                    self.db_conn.rollback()
                    print(f"\033[91mFailed to update courier: {err}\033[0m")
            else:
                self.clear_screen()
                print("\033[93mNo changes made.\033[0m")
        else:
            print("\033[91mInvalid courier index.\033[0m")

    def delete_courier(self):
        self.print_courier_list()
        index = get_valid_input(int, "Enter the index of the courier to delete: ", "Invalid input. Please enter a valid index.") - 1
    
        if 0 <= index < len(self.courier_list):
            courier = self.courier_list[index]
            courier_id = courier['id']
    
            confirmation = get_valid_input(str, f"Are you sure you want to delete the courier '{courier['name']}'? (y/n): ", "Invalid input. Please enter 'y' or 'n'.", pattern=r'^(y|n)$')
            if confirmation.lower() == 'y':
                try:
                    cursor = self.db_conn.cursor()
                    cursor.execute("START TRANSACTION")

                    # Delete associated orders
                    cursor.execute("DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE courier = %s)", (courier_id,))
                    cursor.execute("DELETE FROM orders WHERE courier = %s", (courier_id,))

                    # Delete courier
                    cursor.execute("DELETE FROM couriers WHERE id = %s", (courier_id,))

                    self.db_conn.commit()
                    cursor.close()
                    print("\033[92mCourier and associated orders deleted successfully!\033[0m")
                    self.load_data()
                except mysql.connector.Error as err:
                    self.db_conn.rollback()
                    print(f"\033[91mFailed to delete courier: {err}\033[0m")
            else:
                print("\033[93mCourier deletion cancelled.\033[0m")
        else:
            print("\033[91mInvalid courier index.\033[0m")


    
    def print_customer_list(self):
        self.load_data()  # Ensure data is loaded before printing
        print("\033[93mCustomer List:\033[0m")
        if not self.customer_list:
            print("\033[90mEmpty\033[0m")
        else:
            max_name_length = max(len(customer['name']) for customer in self.customer_list)
            max_address_length = max(len(customer['address']) for customer in self.customer_list)
            max_phone_length = max(len(customer['phone']) for customer in self.customer_list)
            max_index_length = len(str(len(self.customer_list)))
            for i, customer in enumerate(self.customer_list, start=1):
                index_str = str(i).rjust(max_index_length)
                name = customer['name'].ljust(max_name_length)
                address = customer['address'].ljust(max_address_length)
                phone = customer['phone'].ljust(max_phone_length)
                print(f"{index_str}. \033[90mName:\033[0m {name}     \033[90mAddress:\033[0m {address}       \033[90mPhone:\033[0m {phone}")

    def create_customer(self):
        name = get_valid_input(str, "Enter customer name: ", "Invalid input. Please enter a valid name.")
        address = get_valid_input(str, "Enter customer address: ", "Invalid input. Please enter a valid address.")
        phone = get_valid_input(str, "Enter customer phone number: ", "Invalid input. Please enter a valid phone number.", pattern=r'^\+?1?\d{9,15}$')
    
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("START TRANSACTION")  # Explicitly start the transaction
            cursor.execute("INSERT INTO customers (name, address, phone) VALUES (%s, %s, %s)", (name, address, phone))
            self.db_conn.commit()
            cursor.close()
            print("\033[92mCustomer added successfully!\033[0m")
            self.load_data()
        except mysql.connector.Error as err:
            self.db_conn.rollback()
            print(f"\033[91mFailed to add customer: {err}\033[0m")

    def update_customer(self):
        self.print_customer_list()
        index = get_valid_input(int, "Enter the index of the customer to update: ", "Invalid input. Please enter a valid index.") - 1

        if 0 <= index < len(self.customer_list):
            customer = self.customer_list[index]
            customer_id = customer['id']
            updates = {}

            # Collect updates
            for key in ['name', 'address', 'phone']:
                value = input(f"Enter new {key} (Leave blank to keep: {customer[key]}): ")
                if value:
                    updates[key] = value

            # Check if there are any updates
            if updates:
                try:
                    cursor = self.db_conn.cursor()
                    cursor.execute("START TRANSACTION")
                    # Create update query dynamically
                    update_query = ", ".join([f"{k} = %s" for k in updates.keys()])
                    cursor.execute(f"UPDATE customers SET {update_query} WHERE id = %s", (*updates.values(), customer_id))
                    self.db_conn.commit()
                    cursor.close()
                    self.clear_screen()
                    print("\033[92mCustomer updated successfully!\033[0m")
                    self.load_data()
                except mysql.connector.Error as err:
                    self.db_conn.rollback()
                    print(f"\033[91mFailed to update customer: {err}\033[0m")
            else:
                self.clear_screen()
                print("\033[93mNo changes made.\033[0m")
        else:
            print("\033[91mInvalid customer index.\033[0m")

    def delete_customer(self):
        self.print_customer_list()
        index = get_valid_input(int, "Enter the index of the customer to delete: ", "Invalid input. Please enter a valid index.") - 1

        if 0 <= index < len(self.customer_list):
            customer = self.customer_list[index]
            customer_id = customer['id']

            confirmation = get_valid_input(str, f"Are you sure you want to delete the customer '{customer['name']}'? (y/n): ", "Invalid input. Please enter 'y' or 'n'.", pattern=r'^(y|n)$')
            if confirmation.lower() == 'y':
                try:
                    cursor = self.db_conn.cursor()
                    cursor.execute("START TRANSACTION")

                    # Delete associated orders
                    cursor.execute("DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE customer_id = %s)", (customer_id,))
                    cursor.execute("DELETE FROM orders WHERE customer_id = %s", (customer_id,))

                    # Delete customer
                    cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))

                    self.db_conn.commit()
                    cursor.close()
                    print("\033[92mCustomer and associated orders deleted successfully!\033[0m")
                    self.load_data()
                except mysql.connector.Error as err:
                    self.db_conn.rollback()
                    print(f"\033[91mFailed to delete customer: {err}\033[0m")
            else:
                print("\033[93mCustomer deletion cancelled.\033[0m")
        else:
            print("\033[91mInvalid customer index.\033[0m")


    
    def print_order_list(self):
        cursor = self.db_conn.cursor(dictionary=True)

        # Prompt for filter option
        filter_option = get_valid_input(
            int,
            "Filter orders by:\n 0. No Filter\n 1. Status\n 2. Courier\nSelect an option: ",
            "Invalid input. Please enter a valid option.",
            pattern=r'^[0-2]$'
        )

        self.clear_screen()

        filter_clause = ""
        filter_value = None

        if filter_option == 1:
            print("Order Status List:")
            for i, status in enumerate(self.order_status_list, start=1):
                print(f"{i}. {status}")
            status_index = get_valid_input(int, "Enter the index of the status to filter by: ", "Invalid input. Please enter a valid status index.") - 1
            if 0 <= status_index < len(self.order_status_list):
                filter_clause = "WHERE os.order_status = %s"
                filter_value = self.order_status_list[status_index]
            else:
                print("\033[91mInvalid status index.\033[0m")
                return

        elif filter_option == 2:
            self.print_courier_list()
            courier_index = get_valid_input(int, "Enter the index of the courier to filter by: ", "Invalid input. Please enter a valid courier index.") - 1
            if 0 <= courier_index < len(self.courier_list):
                filter_clause = "WHERE c.id = %s"
                filter_value = self.courier_list[courier_index]['id']
            else:
                print("\033[91mInvalid courier index.\033[0m")
                return

        # Query to join orders with customers, couriers, and order status
        query = f"""
        SELECT 
            o.id,
            cu.name AS customer_name,
            cu.address AS customer_address,
            cu.phone AS customer_phone,
            c.name AS courier_name,
            os.order_status AS status_name,
            GROUP_CONCAT(p.name ORDER BY p.id ASC SEPARATOR ', ') AS product_names
        FROM orders o
        LEFT JOIN customers cu ON o.customer_id = cu.id
        LEFT JOIN couriers c ON o.courier = c.id
        LEFT JOIN order_status os ON o.status = os.id
        LEFT JOIN order_items oi ON o.id = oi.order_id
        LEFT JOIN products p ON oi.product_id = p.id
        {filter_clause}
        GROUP BY o.id
        """

        if filter_clause:
            cursor.execute(query, (filter_value,))
        else:
            cursor.execute(query)

        orders = cursor.fetchall()
        cursor.close()

        self.order_index_map = {i + 1: order['id'] for i, order in enumerate(orders)}

        print("\033[93mOrder List:\033[0m")
        if not orders:
            print("\033[90mEmpty\033[0m")
        else:
            max_name_length = max(len(order['customer_name']) for order in orders)
            max_address_length = max(len(order['customer_address']) for order in orders)
            max_phone_length = max(len(order['customer_phone']) for order in orders)
            max_courier_length = max(len(order['courier_name']) for order in orders)
            max_status_length = max(len(order['status_name']) for order in orders)
            max_items_length = max(len(order['product_names']) for order in orders)
            max_index_length = len(str(len(orders)))

            for i, order in enumerate(orders, start=1):
                index_str = str(i).rjust(max_index_length)
                customer_name = order['customer_name'].ljust(max_name_length)
                customer_address = order['customer_address'].ljust(max_address_length)
                customer_phone = order['customer_phone'].ljust(max_phone_length)
                courier_name = order['courier_name'].ljust(max_courier_length)
                status_name = order['status_name'].ljust(max_status_length)
                product_names = order['product_names'].ljust(max_items_length)

                print(f"{index_str}. \033[90mCustomer:\033[0m {customer_name}     "
                      f"\033[90mAddress:\033[0m {customer_address}       "
                      f"\033[90mPhone:\033[0m {customer_phone}       "
                      f"\033[90mCourier:\033[0m {courier_name}       "
                      f"\033[90mStatus:\033[0m {status_name}       "
                      f"\033[90mItems:\033[0m {product_names}")

    def create_order(self):
        self.print_customer_list()
        customer_index = get_valid_input(int, "Select a customer by their index: ", "Invalid input. Please enter a valid customer index.") - 1

        if 0 <= customer_index < len(self.customer_list):
            selected_customer = self.customer_list[customer_index]['id']
        else:
            print("\033[91mInvalid customer index.\033[0m")
            return

        self.print_product_list()
        item_indices = input("Select products by index (comma-separated): ").split(',')
        selected_items = []

        for index in item_indices:
            try:
                index = int(index.strip()) - 1
                if 0 <= index < len(self.product_list):
                    selected_items.append(self.product_list[index]['id'])
                else:
                    print(f"\033[91mInvalid product index: {index + 1}\033[0m")
            except ValueError:
                print(f"\033[91mInvalid input: {index}\033[0m")

        if not selected_items:
            print("\033[91mNo valid products selected.\033[0m")
            return

        self.print_courier_list()
        courier_index = get_valid_input(int, "Enter courier index: ", "Invalid input. Please enter a valid courier index.") - 1

        if 0 <= courier_index < len(self.courier_list):
            selected_courier = self.courier_list[courier_index]['id']
        else:
            print("\033[91mInvalid courier index.\033[0m")
            return

        status = 1  # Default status 'PREPARING'

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("START TRANSACTION")

            cursor.execute("INSERT INTO orders (customer_id, courier, status) VALUES (%s, %s, %s)",
                           (selected_customer, selected_courier, status))
            order_id = cursor.lastrowid
            for product_id in selected_items:
                cursor.execute("INSERT INTO order_items (order_id, product_id) VALUES (%s, %s)", (order_id, product_id))
                # Update inventory
                cursor.execute("UPDATE products SET inventory = inventory - 1 WHERE id = %s", (product_id,))

            self.db_conn.commit()
            cursor.close()
            self.load_data()

            # Clear screen before displaying success message
            self.clear_screen()
            print("\033[92mOrder added successfully!\033[0m")
        except mysql.connector.Error as err:
            self.db_conn.rollback()
            print(f"\033[91mFailed to create order: {err}\033[0m")

    def update_order_status(self):
        self.print_order_list()
        display_order_id = get_valid_input(int, "Enter the order ID to update: ", "Invalid input. Please enter a valid ID.")

        # Map the display ID to actual ID
        actual_order_id = self.order_index_map.get(display_order_id)
        if actual_order_id is None:
            print("\033[91mInvalid order ID.\033[0m")
            return

        print("Order Status List:")
        for i, status in enumerate(self.order_status_list, start=1):
            print(f"{i}. {status}")
        status_index = get_valid_input(int, "Enter the index of the new status: ", "Invalid input. Please enter a valid status index.") - 1

        if 0 <= status_index < len(self.order_status_list):
            new_status = self.order_status_list[status_index]
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("START TRANSACTION")
                cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, actual_order_id))
                self.db_conn.commit()
                cursor.close()
                self.load_data()
                print("\033[92mOrder status updated successfully!\033[0m")
            except mysql.connector.Error as err:
                self.db_conn.rollback()
                print(f"\033[91mFailed to update order status: {err}\033[0m")
        else:
            print("Invalid status index.")

    def update_order(self):
        self.print_order_list()
        display_order_id = get_valid_input(int, "Enter the order ID to update: ", "Invalid input. Please enter a valid ID.")

        # Map the display ID to actual ID
        actual_order_id = self.order_index_map.get(display_order_id)
        if actual_order_id is None:
            print("\033[91mInvalid order ID.\033[0m")
            return

        cursor = self.db_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE id = %s", (actual_order_id,))
        order = cursor.fetchone()
        cursor.close()

        if order:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("START TRANSACTION")

                self.print_customer_list()
                customer_index = get_valid_input(int, f"Select a new customer by index (Leave blank to keep current): ", "Invalid input. Please enter a valid index.", allow_empty=True)
                if customer_index:
                    customer_index -= 1
                    if 0 <= customer_index < len(self.customer_list):
                        order['customer_id'] = self.customer_list[customer_index]['id']

                self.print_product_list()
                selected_product_indices = input(f"Select new products by index (Leave blank to keep current): ")

                # Validate product indices
                if selected_product_indices:
                    valid_product_ids = {product['id'] for product in self.product_list}
                    selected_indices = [idx.strip() for idx in selected_product_indices.split(',') if idx.strip().isdigit()]
                    items = []
                    invalid_indices = []

                    for idx in selected_indices:
                        idx = int(idx)
                        if 1 <= idx <= len(self.product_list):
                            product_id = self.product_list[idx - 1]['id']
                            if product_id in valid_product_ids:
                                items.append(product_id)
                            else:
                                invalid_indices.append(str(idx))
                        else:
                            invalid_indices.append(str(idx))

                    if invalid_indices:
                        print(f"\033[91mInvalid product indices: {', '.join(invalid_indices)}\033[0m")
                        return

                    cursor.execute("DELETE FROM order_items WHERE order_id = %s", (actual_order_id,))
                    for product_id in items:
                        cursor.execute("INSERT INTO order_items (order_id, product_id) VALUES (%s, %s)", (actual_order_id, product_id))
                        cursor.execute("UPDATE products SET inventory = inventory - 1 WHERE id = %s", (product_id,))

                self.print_courier_list()
                courier_index = get_valid_input(int, f"Select new courier by index (Leave blank to keep current): ", "Invalid input. Please enter a valid index.", allow_empty=True)
                if courier_index:
                    courier_index -= 1
                    if 0 <= courier_index < len(self.courier_list):
                        order['courier'] = self.courier_list[courier_index]['id']

                cursor.execute("UPDATE orders SET customer_id = %s, courier = %s WHERE id = %s",
                               (order['customer_id'], order['courier'], actual_order_id))
                self.db_conn.commit()
                cursor.close()
                self.load_data()
                print("\033[92mOrder updated successfully!\033[0m")
            except mysql.connector.Error as err:
                self.db_conn.rollback()
                print(f"\033[91mFailed to update order: {err}\033[0m")
        else:
            print("\033[91mInvalid order ID.\033[0m")

    def delete_order(self):
        self.print_order_list()
        display_order_id = get_valid_input(int, "Enter the order index you wish to delete: ", "Invalid input. Please enter a valid ID.")

        actual_order_id = self.order_index_map.get(display_order_id)
        if actual_order_id is None:
            print("\033[91mInvalid order ID.\033[0m")
            return

        confirmation = get_valid_input(str, f"Are you sure you want to delete the order ID {display_order_id}? (y/n): ", "Invalid input. Please enter 'y' or 'n'.", pattern=r'^(y|n)$')
        if confirmation.lower() == 'y':
            try:
                cursor = self.db_conn.cursor(dictionary=True)
                cursor.execute("START TRANSACTION")

                cursor.execute("SELECT product_id FROM order_items WHERE order_id = %s", (actual_order_id,))
                product_ids = cursor.fetchall()

                cursor.execute("DELETE FROM order_items WHERE order_id = %s", (actual_order_id,))
                for product in product_ids:
                    cursor.execute("UPDATE products SET inventory = inventory + 1 WHERE id = %s", (product['product_id'],))
                cursor.execute("DELETE FROM orders WHERE id = %s", (actual_order_id,))

                self.db_conn.commit()
                cursor.close()
                self.load_data()
                print("\033[92mOrder deleted successfully!\033[0m")
            except mysql.connector.Error as err:
                self.db_conn.rollback()
                print(f"\033[91mFailed to delete order: {err}\033[0m")
        else:
            print("\033[93mOrder deletion cancelled.\033[0m")

    
    def export_to_csv(self, table_name, file_name):
        cursor = self.db_conn.cursor(dictionary=True)

        if table_name == 'orders':
            query = """
            SELECT
                o.id,
                cu.name AS customer_name,
                co.name AS courier_name,
                os.order_status AS status,
                GROUP_CONCAT(p.name ORDER BY p.id ASC SEPARATOR ', ') AS products
            FROM orders o
            JOIN customers cu ON o.customer_id = cu.id
            JOIN couriers co ON o.courier = co.id
            JOIN order_status os ON o.status = os.id
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            GROUP BY o.id
            """
            cursor.execute(query)
        else:
            cursor.execute(f"SELECT * FROM {table_name}")

        rows = cursor.fetchall()
        cursor.close()

        # Ensure the export directory exists
        export_dir = "export"
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        file_path = os.path.join(export_dir, file_name)

        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"\033[92mData exported to {file_path} successfully!\033[0m")

    def import_from_csv(self, table_name, file_name):
        # Ensure the import directory exists
        import_dir = "import"
        if not os.path.exists(import_dir):
            os.makedirs(import_dir)

        file_path = os.path.join(import_dir, file_name)

        if not os.path.exists(file_path):
            print(f"\033[91mFile '{file_path}' does not exist.\033[0m")
            return

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        if not rows:
            print(f"\033[91mFile '{file_path}' is empty or has invalid content.\033[0m")
            return

        cursor = self.db_conn.cursor()

        if table_name == 'orders':
            for row in rows:
                customer_id = self.get_id_by_name('customers', 'name', row['customer_name'])
                courier_id = self.get_id_by_name('couriers', 'name', row['courier_name'])
                status_id = self.get_id_by_name('order_status', 'order_status', row['status'])
                product_names = row['products'].split(', ')

                if customer_id is None or courier_id is None or status_id is None:
                    print(f"\033[91mError: Could not resolve IDs for row: {row}\033[0m")
                    continue

                # Prepare the row data for insertion
                order_data = {
                    'customer_id': customer_id,
                    'courier': courier_id,
                    'status': status_id,
                }

                # Construct the query
                columns = order_data.keys()
                placeholders = ', '.join(['%s'] * len(columns))
                columns_str = ', '.join(columns)
                update_placeholders = ', '.join([f"{col} = VALUES({col})" for col in columns])

                values = tuple(order_data.values())
                query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders}) " \
                        f"ON DUPLICATE KEY UPDATE {update_placeholders}"
                try:
                    cursor.execute(query, values)
                    order_id = cursor.lastrowid if cursor.lastrowid != 0 else self.get_existing_order_id(cursor, customer_id, courier_id, status_id)

                    # Insert products
                    cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
                    for product_name in product_names:
                        product_id = self.get_id_by_name('products', 'name', product_name)
                        if product_id:
                            cursor.execute("INSERT INTO order_items (order_id, product_id) VALUES (%s, %s)", (order_id, product_id))
                except mysql.connector.Error as err:
                    print(f"\033[91mError: {err}\033[0m")
                    self.db_conn.rollback()
                    cursor.close()
                    return

        else:
            columns = rows[0].keys()
            placeholders = ', '.join(['%s'] * len(columns))
            columns_str = ', '.join(columns)
            update_placeholders = ', '.join([f"{col} = VALUES({col})" for col in columns])

            for row in rows:
                values = tuple(row.values())
                query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders}) " \
                        f"ON DUPLICATE KEY UPDATE {update_placeholders}"
                try:
                    cursor.execute(query, values)
                except mysql.connector.Error as err:
                    print(f"\033[91mError: {err}\033[0m")
                    self.db_conn.rollback()
                    cursor.close()
                    return

        self.db_conn.commit()
        cursor.close()

        print(f"\033[92mData imported from {file_path} successfully!\033[0m")

    def get_id_by_name(self, table, column, value):
        cursor = self.db_conn.cursor(dictionary=True)
        cursor.execute(f"SELECT id FROM {table} WHERE {column} = %s", (value,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result['id']
        else:
            return None

    def get_existing_order_id(self, cursor, customer_id, courier_id, status_id):
        cursor.execute("SELECT id FROM orders WHERE customer_id = %s AND courier = %s AND status = %s", (customer_id, courier_id, status_id))
        result = cursor.fetchone()
        if result:
            return result['id']
        else:
            return None



    
    def run(self):
        self.load_data()

        while True:
            self.display_main_menu()
            user_input = get_valid_input(int, "Select an option: ", "Invalid input. Please enter a valid option.", pattern=r'^[0-5]$')

            if user_input == 0:
                self.clear_screen()
                print("Exiting...")
                break
            elif user_input == 1:
                self.clear_screen()
                while True:
                    self.display_product_menu()
                    user_input = get_valid_input(int, "Select an option: ", "Invalid input. Please enter a valid option.", pattern=r'^[0-4]$')

                    if user_input == 0:
                        self.clear_screen()
                        break
                    elif user_input == 1:
                        self.clear_screen()
                        self.print_product_list()
                    elif user_input == 2:
                        self.clear_screen()
                        self.create_product()
                    elif user_input == 3:
                        self.clear_screen()
                        self.update_product()
                    elif user_input == 4:
                        self.clear_screen()
                        self.delete_product()
            elif user_input == 2:
                self.clear_screen()
                while True:
                    self.display_courier_menu()
                    user_input = get_valid_input(int, "Select an option: ", "Invalid input. Please enter a valid option.", pattern=r'^[0-4]$')

                    if user_input == 0:
                        self.clear_screen()
                        break
                    elif user_input == 1:
                        self.clear_screen()
                        self.print_courier_list()
                    elif user_input == 2:
                        self.clear_screen()
                        self.create_courier()
                    elif user_input == 3:
                        self.clear_screen()
                        self.update_courier()
                    elif user_input == 4:
                        self.clear_screen()
                        self.delete_courier()
            elif user_input == 3:
                self.clear_screen()
                while True:
                    self.display_customer_menu()
                    user_input = get_valid_input(int, "Select an option: ", "Invalid input. Please enter a valid option.", pattern=r'^[0-4]$')

                    if user_input == 0:
                        self.clear_screen()
                        break
                    elif user_input == 1:
                        self.clear_screen()
                        self.print_customer_list()
                    elif user_input == 2:
                        self.clear_screen()
                        self.create_customer()
                    elif user_input == 3:
                        self.clear_screen()
                        self.update_customer()
                    elif user_input == 4:
                        self.clear_screen()
                        self.delete_customer()
            elif user_input == 4:
                self.clear_screen()
                while True:
                    self.display_order_menu()
                    user_input = get_valid_input(int, "Select an option: ", "Invalid input. Please enter a valid option.", pattern=r'^[0-5]$')

                    if user_input == 0:
                        self.clear_screen()
                        break
                    elif user_input == 1:
                        self.clear_screen()
                        self.print_order_list()
                    elif user_input == 2:
                        self.clear_screen()
                        self.create_order()
                    elif user_input == 3:
                        self.clear_screen()
                        self.update_order_status()
                    elif user_input == 4:
                        self.clear_screen()
                        self.update_order()
                    elif user_input == 5:
                        self.clear_screen()
                        self.delete_order()
            elif user_input == 5:
                self.clear_screen()
                while True:
                    self.display_data_import_export_menu()
                    user_input = get_valid_input(int, "Select an option: ", "Invalid input. Please enter a valid option.", pattern=r'^[0-2]$')

                    if user_input == 0:
                        self.clear_screen()
                        break
                    elif user_input == 1:
                        self.clear_screen()
                        while True:
                            self.display_export_menu()
                            user_input = get_valid_input(int, "Select an option: ", "Invalid input. Please enter a valid option.", pattern=r'^[0-4]$')
                            if user_input == 0:
                                self.clear_screen()
                                break
                            elif user_input == 1:
                                self.clear_screen()
                                self.export_to_csv('products', 'products.csv')
                            elif user_input == 2:
                                self.clear_screen()
                                self.export_to_csv('couriers', 'couriers.csv')
                            elif user_input == 3:
                                self.clear_screen()
                                self.export_to_csv('customers', 'customers.csv')
                            elif user_input == 4:
                                self.clear_screen()
                                self.export_to_csv('orders', 'orders.csv')
                    elif user_input == 2:
                        self.clear_screen()
                        while True:
                            self.display_import_menu()
                            user_input = get_valid_input(int, "Select an option: ", "Invalid input. Please enter a valid option.", pattern=r'^[0-4]$')
                            if user_input == 0:
                                self.clear_screen()
                                break
                            elif user_input == 1:
                                self.clear_screen()
                                self.import_from_csv('products', 'products.csv')
                            elif user_input == 2:
                                self.clear_screen()
                                self.import_from_csv('couriers', 'couriers.csv')
                            elif user_input == 3:
                                self.clear_screen()
                                self.import_from_csv('customers', 'customers.csv')
                            elif user_input == 4:
                                self.clear_screen()
                                self.import_from_csv('orders', 'orders.csv')

if __name__ == "__main__":
    app = CafeApp()
    app.run()
    app.clear_screen
