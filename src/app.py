import os
import csv
import re

def get_valid_input(input_type, prompt, error_message, pattern=None, default_value=None, allow_empty=False):
    while True:
        value = input(prompt)

        # Check for empty input
        if not value:
            if allow_empty:
                return default_value if default_value is not None else ""
            else:
                print(error_message)
                continue

        # Check for pattern match (if provided)
        if pattern:
            if re.match(pattern, value):
                try:
                    return input_type(value)
                except ValueError:
                    print(error_message)
                    continue
            else:
                print(error_message)
                continue

        # If no pattern is provided, just try to convert to the desired input_type
        try:
            return input_type(value)
        except ValueError:
            print(error_message)
            continue


class CafeApp:
    def __init__(self):
        self.product_list = []
        self.courier_list = []
        self.order_list = []
        self.order_status_list = ["PREPARING", "READY", "DELIVERED"]
        self.data_dir = os.path.join(os.getcwd(), "data")  # Use the current working directory and join "data"
        self.products_file = os.path.join(self.data_dir, "products.csv")
        self.couriers_file = os.path.join(self.data_dir, "couriers.csv")
        self.orders_file = os.path.join(self.data_dir, "orders.csv")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_data(self):
        if os.path.exists(self.products_file):
            with open(self.products_file, "r") as file:
                reader = csv.DictReader(file)
                self.product_list = list(reader)

        if os.path.exists(self.couriers_file):
            with open(self.couriers_file, "r") as file:
                reader = csv.DictReader(file)
                self.courier_list = list(reader)

        if os.path.exists(self.orders_file):
            with open(self.orders_file, "r") as file:
                reader = csv.DictReader(file)
                self.order_list = list(reader)

    def save_data(self):
        with open(self.products_file, "w", newline='') as file:
            fieldnames = ["name", "price"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.product_list)

        with open(self.couriers_file, "w", newline='') as file:
            fieldnames = ["name", "phone"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.courier_list)

        with open(self.orders_file, "w", newline='') as file:
            fieldnames = ["customer_name", "customer_address", "customer_phone", "courier", "status", "items"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.order_list)

    def display_main_menu(self):
        main_menu = (f"Main Menu"
                     "\n 0. Exit application"
                     "\n 1. Product Menu"
                     "\n 2. Courier Menu"
                     "\n 3. Orders Menu")
        print(main_menu)

    def display_product_menu(self):
        product_menu = (f"Product Menu"
                        "\n 0 - Return to Main Menu"
                        "\n 1 - Print Products List"
                        "\n 2 - Create New Product"
                        "\n 3 - Update Existing Product"
                        "\n 4 - Delete Product")
        print(product_menu)

    def display_courier_menu(self):
        courier_menu = (f"Courier Menu"
                        "\n 0 - Return to Main Menu"
                        "\n 1 - Print Couriers List"
                        "\n 2 - Create New Courier"
                        "\n 3 - Update Existing Courier"
                        "\n 4 - Delete Courier")
        print(courier_menu)

    def display_order_menu(self):
        order_menu = (f"Order Menu"
                      "\n 0 - Return to Main Menu"
                      "\n 1 - Print Order List"
                      "\n 2 - Create Order"
                      "\n 3 - Update Existing Order Status"
                      "\n 4 - Update Existing Order"
                      "\n 5 - Delete Order")
        print(order_menu)

    def print_product_list(self):
        print("Product List:")
        for i, product in enumerate(self.product_list, start=1):
            print(f"{i}. {product['name']} - £{product['price']}")

    def create_product(self):
        name = get_valid_input(str, "Enter product name: ", "Invalid input. Please enter a valid name.")
        price = get_valid_input(float, "Enter product price: ", "Invalid input. Please enter a valid price.", pattern=r'^\d+(\.\d{1,2})?$')
        product = {"name": name, "price": price}
        self.product_list.append(product)
        self.save_data()
        print("Product added successfully!")

    def update_product(self):
        self.print_product_list()
        index = get_valid_input(int, "Enter the index of the product to update: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.product_list):
            product = self.product_list[index]
            for key in product:
                value = input(f"Enter new {key} (leave blank to keep current value: {product[key]}): ")
                if value:
                    product[key] = value
            self.save_data()
            print("Product updated successfully!")
        else:
            print("Invalid product index.")

    def delete_product(self):
        self.print_product_list()
        index = get_valid_input(int, "Enter the index of the product to delete: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.product_list):
            del self.product_list[index]
            self.save_data()
            print("Product deleted successfully!")
        else:
            print("Invalid product index.")

    def print_courier_list(self):
        print("Courier List:")
        for i, courier in enumerate(self.courier_list, start=1):
            print(f"{i}. {courier['name']} - {courier['phone']}")

    def create_courier(self):
        name = get_valid_input(str, "Enter courier name: ", "Invalid input. Please enter a valid name.")
        phone = get_valid_input(str, "Enter courier phone number: ", "Invalid input. Please enter a valid phone number.", pattern=r'^\+?1?\d{9,15}$')
        courier = {"name": name, "phone": phone}
        self.courier_list.append(courier)
        self.save_data()
        print("Courier added successfully!")

    def update_courier(self):
        self.print_courier_list()
        index = get_valid_input(int, "Enter the index of the courier to update: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.courier_list):
            courier = self.courier_list[index]
            for key in courier:
                value = input(f"Enter new value for {key} (leave blank to keep current value: {courier[key]}): ")
                if value:
                    courier[key] = value
            self.save_data()
            print("Courier updated successfully!")
        else:
            print("Invalid courier index.")

    def delete_courier(self):
        self.print_courier_list()
        index = get_valid_input(int, "Enter the index of the courier to delete: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.courier_list):
            del self.courier_list[index]
            self.save_data()
            print("Courier deleted successfully!")
        else:
            print("Invalid courier index.")

    def print_order_list(self):
        print("Order List:")
        for i, order in enumerate(self.order_list, start=1):
            print(f"{i}. Customer: {order['customer_name']}, Address: {order['customer_address']}, Phone: {order['customer_phone']}, Courier: {order['courier']}, Status: {order['status']}, Items: {order['items']}")

    def create_order(self):
        customer_name = get_valid_input(str, "Enter customer name: ", "Invalid input. Please enter a valid name.")
        customer_address = get_valid_input(str, "Enter customer address: ", "Invalid input. Please enter a valid address.")
        customer_phone = get_valid_input(str, "Enter customer phone number: ", "Invalid input. Please enter a valid phone number.", pattern=r'^\+?1?\d{9,15}$')

        self.print_product_list()
        items = get_valid_input(str, "Select a product: ", "Invalid input. Please enter a valid product index.")

        self.print_courier_list()
        courier = get_valid_input(str, "Enter courier index: ", "Invalid input. Please enter a valid courier index.")

        status = "PREPARING"

        order = {
            "customer_name": customer_name,
            "customer_address": customer_address,
            "customer_phone": customer_phone,
            "courier": courier,
            "status": status,
            "items": items
        }
        self.order_list.append(order)
        self.save_data()
        print("Order added successfully!")

    def update_order_status(self):
        self.print_order_list()
        index = get_valid_input(int, "Enter the index of the order to update: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.order_list):
            order = self.order_list[index]
            print("Order Status List:")
            for i, status in enumerate(self.order_status_list, start=1):
                print(f"{i}. {status}")
            status_index = get_valid_input(int, "Enter the index of the new status: ", "Invalid input. Please enter a valid status index.") - 1
            if 0 <= status_index < len(self.order_status_list):
                order["status"] = self.order_status_list[status_index]
                self.save_data()
                print("Order status updated successfully!")
            else:
                print("Invalid status index.")
        else:
            print("Invalid order index.")

    def update_order(self):
        self.print_order_list()
        index = get_valid_input(int, "Enter the index of the order to update: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.order_list):
            order = self.order_list[index]
            for key in order:
                if key == "items":
                    self.print_product_list()
                    value = input(f"Enter new comma-separated list of product indexes (leave blank to keep current value: {order[key]}): ")
                elif key == "courier":
                    self.print_courier_list()
                    value = input(f"Enter new courier index (leave blank to keep current value: {order[key]}): ")
                else:
                    value = input(f"Enter new value for {key} (leave blank to keep current value: {order[key]}): ")
                if value:
                    order[key] = value
            self.save_data()
            print("Order updated successfully!")
        else:
            print("Invalid order index.")

    def delete_order(self):
        self.print_order_list()
        index = get_valid_input(int, "Enter the index of the order to delete: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.order_list):
            del self.order_list[index]
            self.save_data()
            print("Order deleted successfully!")
        else:
            print("Invalid order index.")

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
