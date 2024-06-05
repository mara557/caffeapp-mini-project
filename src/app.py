import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
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
                     "\n 3. Orders Menu")
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
                print(f"{index_str}. {name} £{product['price']}")

    def create_product(self):
        name = get_valid_input(str, "Enter product name: ", "Invalid input. Please enter a valid name.")
        price = get_valid_input(float, "Enter product price: ", "Invalid input. Please enter a valid price.", pattern=r'^\d+(\.\d{1,2})?$')
        
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
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
            cursor.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (product['name'], product['price'], product_id))
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

    def print_order_list(self):
        cursor = self.db_conn.cursor(dictionary=True)

        # Query to join orders with couriers and order status
        query = """
        SELECT 
            o.id,
            o.customer_name,
            o.customer_address,
            o.customer_phone,
            c.name AS courier_name,
            os.order_status AS status_name,
            o.items
        FROM orders o
        LEFT JOIN couriers c ON o.courier = c.id
        LEFT JOIN order_status os ON o.status = os.id
        """

        cursor.execute(query)
        orders = cursor.fetchall()

        # Fetch all product names and map them by their ID
        cursor.execute("SELECT id, name FROM products")
        products = cursor.fetchall()
        cursor.close()
        product_map = {product['id']: product['name'] for product in products}

        print("\033[93mOrder List:\033[0m")
        if not orders:
            print("\033[90mEmpty\033[0m")
        else:
            self.order_index_map = {}  # Reset the index map
            for display_id, order in enumerate(orders, start=1):
                # Create the mapping of display ID to actual ID
                self.order_index_map[display_id] = order['id']
                # Convert product IDs to names
                item_ids = order['items'].split(',')
                item_names = []
                for item_id in item_ids:
                    item_id = item_id.strip()
                    if item_id.isdigit():
                        product_name = product_map.get(int(item_id), "Unknown product")
                        item_names.append(product_name)
                    else:
                        item_names.append("Invalid product ID")

                item_names_str = ", ".join(item_names)

                print(f"{display_id}. "
                      f"Customer: {order['customer_name']} "
                      f"Address: {order['customer_address']} "
                      f"Phone: {order['customer_phone']} "
                      f"Courier: {order['courier_name']} "
                      f"Status: {order['status_name']} "
                      f"Items: {item_names_str}")

    def create_order(self):
        customer_name = get_valid_input(str, "Enter customer name: ", "Invalid input. Please enter a valid name.")
        customer_address = get_valid_input(str, "Enter customer address: ", "Invalid input. Please enter a valid address.")
        customer_phone = get_valid_input(str, "Enter customer phone number: ", "Invalid input. Please enter a valid phone number.", pattern=r'^\+?1?\d{9,15}$')

        self.print_product_list()
        item_indices = input("Select products by index (comma-separated): ").split(',')
        selected_items = []

        for index in item_indices:
            try:
                index = int(index.strip()) - 1
                if 0 <= index < len(self.product_list):
                    selected_items.append(str(self.product_list[index]['id']))
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
        cursor.execute("INSERT INTO orders (customer_name, customer_address, customer_phone, courier, status, items) VALUES (%s, %s, %s, %s, %s, %s)",
                       (customer_name, customer_address, customer_phone, selected_courier, status, ','.join(selected_items)))
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
            for key in ['customer_name', 'customer_address', 'customer_phone']:
                value = input(f"Enter new {key} (Leave blank to keep: {order[key]}): ")
                if value:
                    order[key] = value

            # Fetch all product names and map them by their ID
            cursor = self.db_conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name FROM products")
            products = cursor.fetchall()
            cursor.close()
            product_map = {product['id']: product['name'] for product in products}

            # Convert existing product IDs in the order to names
            current_product_names = [product_map.get(int(pid.strip()), "Unknown product") for pid in order['items'].split(',')]

            # Display user-friendly product list
            print("\033[93mProduct List:\033[0m")
            for idx, product in enumerate(self.product_list, start=1):
                print(f"{idx}. {product['name']} £{product['price']}")

            selected_product_indices = input(f"Select new products (Leave blank to keep: {', '.join(current_product_names)}): ")

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
                            items.append(str(product_id))
                        else:
                            invalid_indices.append(str(idx))
                    else:
                        invalid_indices.append(str(idx))

                if invalid_indices:
                    print(f"\033[91mInvalid product indices: {', '.join(invalid_indices)}\033[0m")
                    return

                order['items'] = ','.join(items)

            # Fetch all courier names and map them by their ID
            cursor = self.db_conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name FROM couriers")
            couriers = cursor.fetchall()
            cursor.close()
            courier_map = {courier['id']: courier['name'] for courier in couriers}

            # Convert existing courier ID in the order to name
            current_courier_name = courier_map.get(order['courier'], "Unknown courier")

            self.print_courier_list()
            courier_index = get_valid_input(int, f"Enter new courier index (Leave blank to keep: {current_courier_name}): ", "Invalid input. Please enter a valid index.", allow_empty=True)
            if courier_index:
                courier_index -= 1
                if 0 <= courier_index < len(self.courier_list):
                    order['courier'] = self.courier_list[courier_index]['id']

            cursor = self.db_conn.cursor()
            cursor.execute("UPDATE orders SET customer_name = %s, customer_address = %s, customer_phone = %s, courier = %s, items = %s WHERE id = %s",
                           (order['customer_name'], order['customer_address'], order['customer_phone'], order['courier'], order['items'], actual_order_id))
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
        cursor.execute("DELETE FROM orders WHERE id = %s", (actual_order_id,))
        self.db_conn.commit()
        cursor.close()
        self.load_data()
        print("\033[92mOrder deleted successfully!\033[0m")

    def run(self):
        self.load_data()

        while True:
            self.display_main_menu()
            user_input = get_valid_input(int, "Select an option: ", "Invalid input. Please enter a valid option.", pattern=r'^[0-3]$')

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
