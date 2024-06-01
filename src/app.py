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
        print("\033[93mProduct List:\033[0m")
        max_name_length = max(len(product['name']) for product in self.product_list)
        max_index_length = len(str(len(self.product_list)))
        for i, product in enumerate(self.product_list, start=1):
            index_str = str(i).rjust(max_index_length)
            name = product['name'].ljust(max_name_length)
            print(f"{index_str}. {name} £{product['price']}")

    def create_product(self):
        name = get_valid_input(str, "Enter product name: ", "Invalid input. Please enter a valid name.")
        price = get_valid_input(float, "Enter product price: ", "Invalid input. Please enter a valid price.", pattern=r'^\d+(\.\d{1,2})?$')
        product = {"name": name, "price": price}
        self.product_list.append(product)
        self.save_data()
        print("\033[92mProduct added successfully!\033[0m")

    def update_product(self):
        self.print_product_list()
        index = get_valid_input(int, "Enter the index of the product to update: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.product_list):
            product = self.product_list[index]
            for key in product:
                value = input(f"Enter new {key} (leave blank to keep: {product[key]}): ")
                if value:
                    product[key] = value
            self.save_data()
            print("\033[92mProduct updated successfully!\033[0m")
        else:
            print("\033[91mInvalid product index.\033[0m")

    def delete_product(self):
        self.print_product_list()
        index = get_valid_input(int, "Enter the index of the product to delete: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.product_list):
            del self.product_list[index]
            self.save_data()
            print("Product deleted successfully!")
        else:
            print("\033[91mInvalid product index.\033[0m")

    def print_courier_list(self):
        print("\033[93mCourier List:\033[0m")
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
        courier = {"name": name, "phone": phone}
        self.courier_list.append(courier)
        self.save_data()
        print("\033[92mCourier added successfully!\033[0m")

    def update_courier(self):
        self.print_courier_list()
        index = get_valid_input(int, "Enter the index of the courier to update: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.courier_list):
            courier = self.courier_list[index]
            for key in courier:
                value = input(f"Enter new {key} (leave blank to keep: {courier[key]}): ")
                if value:
                    courier[key] = value
            self.save_data()
            print("\033[92mCourier updated successfully!\033[0m")
        else:
            print("\033[91mInvalid courier index.\033[0m")

    def delete_courier(self):
        self.print_courier_list()
        index = get_valid_input(int, "Enter the index of the courier to delete: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.courier_list):
            del self.courier_list[index]
            self.save_data()
            print("Courier deleted successfully!")
        else:
            print("\033[91mInvalid courier index.\033[0m")

    def print_order_list(self):
        print("\033[93mOrder List:\033[0m")
        for i, order in enumerate(self.order_list, start=1):
            index_padding = " " if i < 10 else ""
            print(f"{index_padding}{i}. "
                  f"\033[90mCustomer:\033[0m {order['customer_name']: <25}"
                  f"\033[90mAddress:\033[0m {order['customer_address']: <40}"
                  f"\033[90mPhone:\033[0m {order['customer_phone']: <15}"
                  f"\033[90mCourier:\033[0m {order['courier']: <15}"
                  f"\033[90mStatus:\033[0m {order['status']: <15}"
                  f"\033[90mItems:\033[0m {order['items']}")

    def create_order(self):
        customer_name = get_valid_input(str, "Enter customer name: ", "Invalid input. Please enter a valid name.")
        customer_address = get_valid_input(str, "Enter customer address: ", "Invalid input. Please enter a valid address.")
        customer_phone = get_valid_input(str, "Enter customer phone number: ", "Invalid input. Please enter a valid phone number.", pattern=r'^\+?1?\d{9,15}$')

        self.print_product_list()
        item_index = get_valid_input(int, "Select a product index: ", "Invalid input. Please enter a valid product index.") - 1
        if 0 <= item_index < len(self.product_list):
            selected_item = self.product_list[item_index]['name']  # Retrieve the name of the selected item
        else:
            print("\033[91mInvalid product index.\033[0m")

            return

        self.print_courier_list()
        courier_index = get_valid_input(int, "Enter courier index: ", "Invalid input. Please enter a valid courier index.") - 1
        if 0 <= courier_index < len(self.courier_list):
            selected_courier = self.courier_list[courier_index]['name']  # Retrieve the name of the selected courier
        else:
            print("\033[91mInvalid courier index.\033[0m")
            return

        status = "PREPARING"

        order = {
            "customer_name": customer_name,
            "customer_address": customer_address,
            "customer_phone": customer_phone,
            "courier": selected_courier,  # Save the name of the selected courier
            "status": status,
            "items": selected_item  # Save the name of the selected item
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
            print("\033[91mInvalid order index.\033[0m")

    def update_order(self):
        self.print_order_list()
        index = get_valid_input(int, "Enter the index of the order to update: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.order_list):
            order = self.order_list[index]
            for key in order:
                if key == "items":
                    self.print_product_list()
                    selected_product_index = get_valid_input(int, f"Select a new product by index (leave blank to keep: {order[key]}): ", "Invalid input. Please enter a valid product index.", allow_empty=True)
                    if selected_product_index:
                        selected_product_index -= 1  # Adjust index only if it's not empty
                        if 0 <= selected_product_index < len(self.product_list):
                            order[key] = self.product_list[selected_product_index]["name"]
                elif key == "courier":
                    self.print_courier_list()
                    selected_courier_index = get_valid_input(int, f"Enter new courier index (leave blank to keep: {order[key]}): ", "Invalid input. Please enter a valid courier index.", allow_empty=True)
                    if selected_courier_index:
                        selected_courier_index -= 1  # Adjust index only if it's not empty
                        if 0 <= selected_courier_index < len(self.courier_list):
                            order[key] = self.courier_list[selected_courier_index]["name"]
                elif key == "status":
                    print("Available Order Statuses:")
                    for i, status in enumerate(self.order_status_list, start=1):
                        print(f"{i}. {status}")
                    selected_status_index = get_valid_input(int, f"Enter new status index (leave blank to keep: {order[key]}): ", "Invalid input. Please enter a valid status index.", allow_empty=True)
                    if selected_status_index:
                        selected_status_index -= 1  # Adjust index only if it's not empty
                        if 0 <= selected_status_index < len(self.order_status_list):
                            order[key] = self.order_status_list[selected_status_index]
                else:
                    value = input(f"Enter new {key} (leave blank to keep: {order[key]}): ")
                    if value:
                        order[key] = value
            self.save_data()
            print("\033[92mOrder updated successfully!\033[0m")
        else:
            print("\033[91mInvalid order index.\033[0m")

    def delete_order(self):
        self.print_order_list()
        index = get_valid_input(int, "Input the index of the order you want to delete: ", "Invalid input. Please enter a valid index.") - 1
        if 0 <= index < len(self.order_list):
            del self.order_list[index]
            self.save_data()
            print("\033[92mOrder deleted successfully!\033[0m")
        else:
            print("\033[91mInvalid order index.\033[0m")

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
