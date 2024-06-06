import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # Make sure to use 'localhost' or '127.0.0.1'
        port=3306,
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

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

    def save_data(self):
        # This method can be used for any additional data persistence needs, but it's not required for orders anymore
        pass

    def display_main_menu(self):
        main_menu = (f"\033[38;2;226;135;67mMain Menu\033[0m"
                     "\n 0. Exit application"
                     "\n 1. Product Menu"
                     "\n 2. Courier Menu"
                     "\n 3. Customer Menu"
                     "\n 4. Orders Menu")
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
                print(f"{index_str}. {name} £{product['price']} (Inventory: {product['inventory']})")

    def create_product(self):
        name = get_valid_input(str, "Enter product name: ", "Invalid input. Please enter a valid name.")
        price = get_valid_input(float, "Enter product price: ", "Invalid input. Please enter a valid price.", pattern=r'^\d+(\.\d{1,2})?$')
        inventory = get_valid_input(int, "Enter product inventory: ", "Invalid input. Please enter a valid inventory.")
        
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO products (name, price, inventory) VALUES (%s, %s, %s)", (name, price, inventory))
        self.db_conn.commit()
        cursor.close()
        
        print("\033[92mProduct added successfully!\033[0m")

    def update_product(self):
        self.print_product_list()
        index = get_valid_input(int, "Enter the index of the product to update: ", "Invalid input. Please enter a valid index.") - 1
        
        if 0 <= index < len(self.product_list):
            product = self.product_list[index]
            product_id = product['id']
            
            for key in product:
                if key != 'id':
                    value = input(f"Enter new {key} (Leave blank to keep: {product[key]}): ")
                    if value:
                        product[key] = value
            
            cursor = self.db_conn.cursor()
            cursor.execute("UPDATE products SET name = %s, price = %s, inventory = %s WHERE id = %s", (product['name'], product['price'], product['inventory'], product_id))
            self.db_conn.commit()
            cursor.close()
            
            print("\033[92mProduct updated successfully!\033[0m")
        else:
            print("\033[91mInvalid product index.\033[0m")

    def delete_product(self):
        self.print_product_list()
        index = get_valid_input(int, "Enter the index of the product to delete: ", "Invalid input. Please enter a valid index.") - 1
        
        if 0 <= index < len(self.product_list):
            product = self.product_list[index]
            product_id = product['id']
            
            cursor = self.db_conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            self.db_conn.commit()
            cursor.close()
            
            print("\033[92mProduct deleted successfully!\033[0m")

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
        
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO couriers (name, phone) VALUES (%s, %s)", (name, phone))
        self.db_conn.commit()
        cursor.close()
        
        print("\033[92mCourier added successfully!\033[0m")
        self.load_data()

    def update_courier(self):
        self.print_courier_list()
        index = get_valid_input(int, "Enter the index of the courier to update: ", "Invalid input. Please enter a valid index.") - 1
        
        if 0 <= index < len(self.courier_list):
            courier = self.courier_list[index]
            courier_id = courier['id']
            
            for key in courier:
                if key != 'id':
                    value = input(f"Enter new {key} (Leave blank to keep: {courier[key]}): ")
                    if value:
                        courier[key] = value
            
            cursor = self.db_conn.cursor()
            cursor.execute("UPDATE couriers SET name = %s, phone = %s WHERE id = %s", (courier['name'], courier['phone'], courier_id))
            self.db_conn.commit()
            cursor.close()
            
            print("\033[92mCourier updated successfully!\033[0m")
            self.load_data()
        else:
            print("\033[91mInvalid courier index.\033[0m")

    def delete_courier(self):
        self.print_courier_list()
        index = get_valid_input(int, "Enter the index of the courier to delete: ", "Invalid input. Please enter a valid index.") - 1
        
        if 0 <= index < len(self.courier_list):
            courier = self.courier_list[index]
            courier_id = courier['id']
            
            cursor = self.db_conn.cursor()
            cursor.execute("DELETE FROM couriers WHERE id = %s", (courier_id,))
            self.db_conn.commit()
            cursor.close()
            
            print("\033[92mCourier deleted successfully!\033[0m")
            self.load_data()
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
                print(f"{index_str}. {name}  {address}  {phone}")

    def create_customer(self):
        name = get_valid_input(str, "Enter customer name: ", "Invalid input. Please enter a valid name.")
        address = get_valid_input(str, "Enter customer address: ", "Invalid input. Please enter a valid address.")
        phone = get_valid_input(str, "Enter customer phone number: ", "Invalid input. Please enter a valid phone number.", pattern=r'^\+?1?\d{9,15}$')
        
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO customers (name, address, phone) VALUES (%s, %s, %s)", (name, address, phone))
        self.db_conn.commit()
        cursor.close()
        
        print("\033[92mCustomer added successfully!\033[0m")
        self.load_data()

    def update_customer(self):
        self.print_customer_list()
        index = get_valid_input(int, "Enter the index of the customer to update: ", "Invalid input. Please enter a valid index.") - 1
        
        if 0 <= index < len(self.customer_list):
            customer = self.customer_list[index]
            customer_id = customer['id']
            
            for key in customer:
                if key != 'id':
                    value = input(f"Enter new {key} (Leave blank to keep: {customer[key]}): ")
                    if value:
                        customer[key] = value
            
            cursor = self.db_conn.cursor()
            cursor.execute("UPDATE customers SET name = %s, address = %s, phone = %s WHERE id = %s", (customer['name'], customer['address'], customer['phone'], customer_id))
            self.db_conn.commit()
            cursor.close()
            
            print("\033[92mCustomer updated successfully!\033[0m")
            self.load_data()
        else:
            print("\033[91mInvalid customer index.\033[0m")

    def delete_customer(self):
        self.print_customer_list()
        index = get_valid_input(int, "Enter the index of the customer to delete: ", "Invalid input. Please enter a valid index.") - 1
        
        if 0 <= index < len(self.customer_list):
            customer = self.customer_list[index]
            customer_id = customer['id']
            
            cursor = self.db_conn.cursor()
            cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
            self.db_conn.commit()
            cursor.close()
            
            print("\033[92mCustomer deleted successfully!\033[0m")
            self.load_data()
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
            for i, order in enumerate(orders, start=1):
                print(f"{i}. "
                      f"Customer: {order['customer_name']} "
                      f"Address: {order['customer_address']} "
                      f"Phone: {order['customer_phone']} "
                      f"Courier: {order['courier_name']} "
                      f"Status: {order['status_name']} "
                      f"Items: {order['product_names']}")

    def create_order(self):
        self.print_customer_list()
        customer_index = get_valid_input(int, "Enter customer index: ", "Invalid input. Please enter a valid customer index.") - 1

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

        cursor = self.db_conn.cursor()
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
        print("\033[92mOrder added successfully!\033[0m")

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
            cursor = self.db_conn.cursor()
            cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, actual_order_id))
            self.db_conn.commit()
            cursor.close()
            self.load_data()
            print("\033[92mOrder status updated successfully!\033[0m")
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
            self.print_customer_list()
            customer_index = get_valid_input(int, f"Enter new customer index (Leave blank to keep current): ", "Invalid input. Please enter a valid index.", allow_empty=True)
            if customer_index:
                customer_index -= 1
                if 0 <= customer_index < len(self.customer_list):
                    order['customer_id'] = self.customer_list[customer_index]['id']

            self.print_product_list()
            selected_product_indices = input(f"Select new products (Leave blank to keep current): ")

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

                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM order_items WHERE order_id = %s", (actual_order_id,))
                for product_id in items:
                    cursor.execute("INSERT INTO order_items (order_id, product_id) VALUES (%s, %s)", (actual_order_id, product_id))
                    cursor.execute("UPDATE products SET inventory = inventory - 1 WHERE id = %s", (product_id,))
                cursor.close()

            self.print_courier_list()
            courier_index = get_valid_input(int, f"Enter new courier index (Leave blank to keep current): ", "Invalid input. Please enter a valid index.", allow_empty=True)
            if courier_index:
                courier_index -= 1
                if 0 <= courier_index < len(self.courier_list):
                    order['courier'] = self.courier_list[courier_index]['id']

            cursor = self.db_conn.cursor()
            cursor.execute("UPDATE orders SET customer_id = %s, courier = %s WHERE id = %s",
                           (order['customer_id'], order['courier'], actual_order_id))
            self.db_conn.commit()
            cursor.close()
            self.load_data()
            print("\033[92mOrder updated successfully!\033[0m")
        else:
            print("\033[91mInvalid order ID.\033[0m")

    def delete_order(self):
        self.print_order_list()
        display_order_id = get_valid_input(int, "Enter the order ID to delete: ", "Invalid input. Please enter a valid ID.")

        # Map the display ID to actual ID
        actual_order_id = self.order_index_map.get(display_order_id)
        if actual_order_id is None:
            print("\033[91mInvalid order ID.\033[0m")
            return

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT product_id FROM order_items WHERE order_id = %s", (actual_order_id,))
        product_ids = cursor.fetchall()

        cursor.execute("DELETE FROM order_items WHERE order_id = %s", (actual_order_id,))
        for product_id in product_ids:
            cursor.execute("UPDATE products SET inventory = inventory + 1 WHERE id = %s", (product_id['product_id'],))
        cursor.execute("DELETE FROM orders WHERE id = %s", (actual_order_id,))
        self.db_conn.commit()
        cursor.close()
        self.load_data()
        print("\033[92mOrder deleted successfully!\033[0m")

    def run(self):
        self.load_data()

        while True:
            self.display_main_menu()
            user_input = get_valid_input(int, "Select an option: ", "Invalid input. Please enter a valid option.", pattern=r'^[0-4]$')

            if user_input == 0:
                self.clear_screen()
                self.save_data()
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

if __name__ == "__main__":
    app = CafeApp()
    app.run()
