# Mini Project Week 6

Let's now maintain all our data in the database. We'll create an orders table and an order status table and refactor our app to make use of it.

## Goals

As a user I want to:

- create a product, courier, or order and add it to a table
- view all products, couriers, or orders
- update the status of an order
- persist my data in a database
- _STRETCH_ delete or update a product, order, or courier
- _BONUS_ display orders by status or courier
- _BONUS_ CRUD a list of customers
- _BONUS_ track my product inventory
- _BONUS_ import/export my entities in CSV format

## Spec

- A row in the `products` table should contain the following information:

```json
{
    "id": 4,
    "name": "Coke Zero",
    "price": 0.8
}
```

- A row in the `couriers` table should contain the following information:

```json
{
    "id": 2,
    "name": "Bob",
    "phone": "0789887889"
}
```

- A row in the `orders` table should contain the following information:

```json
{
    "id": 1,
    "customer_name": "John",
    "customer_address": "Unit 2, 12 Main Street, LONDON, WH1 2ER",
    "customer_phone": "0789887334",
    "courier": 2, // Courier ID
    "status": 1, // Order status ID
    "items": "1, 3, 4" // Product IDs
}
```

- A row in the `order_status` table should contain the following information:

```json
{
    "id": 1,
    "order_status": "preparing"
}
```

```txt
# we are no longer reading products, couriers, orders and order statuses from files
# we are now reading data from database tables

PRINT main menu options
GET user input for main menu option

IF user input is 0:
    EXIT app

# products menu
ELSE IF user input is 1:
    PRINT product menu options
    GET user input for product menu option

    IF user inputs 0:
        RETURN to main menu

    # WEEK 5 UPDATE
    ELSE IF user input is 1:
        GET all products from products table
        PRINT products

    # WEEK 5 UPDATE
    ELSE IF user input is 2:
        # CREATE new product

        GET user input for product name
        GET user input for product price
        INSERT product into products table

    # WEEK 5 UPDATE
    ELSE IF user input is 3:
        # STRETCH GOAL - UPDATE existing product

        GET all products from products table
        PRINT products with their IDs
        GET user input for product ID

        GET user input for product name
        GET user input for product price

        IF any inputs are empty, do not update them
        UPDATE properties for product in product table

    # WEEK 5 UPDATE
    ELSE IF user input is 4:
        # STRETCH GOAL - DELETE product

        GET all products from products table
        PRINT products with their IDs

        GET user input for product ID
        DELETE product in products table

# couriers menu
ELSE IF user input is 2:
    PRINT courier menu options
    GET user input for courier menu option

    IF user inputs 0:
        RETURN to main menu

    # WEEK 5 UPDATE
    ELIF user inputs 1:
        GET all couriers from couriers table
        PRINT couriers

    # WEEK 5 UPDATE
    ELSE IF user input is 2:
        # CREATE new courier

        GET user input for courier name
        GET user input for courier phone number
        INSERT courier into couriers table

    # WEEK 5 UPDATE
    ELSE IF user input is 3:
        # STRETCH GOAL - UPDATE existing courier

        GET all couriers from couriers table
        PRINT couriers with their IDs
        GET user input for courier ID

        GET user input for courier name
        GET user input for courier phone number

        IF an input is empty, do not update its respective table property
        UPDATE properties for courier in courier table

    # WEEK 5 UPDATE
    ELSE IF user input is 4:
        # STRETCH GOAL - DELETE courier

        GET all couriers from couriers table
        PRINT courier with their IDs

        GET user input for courier ID
        DELETE courier in couriers table

# orders menu
ELSE IF user input is 3:
    PRINT order menu options
    GET user input for order menu option

    IF user input is 0:
        RETURN to main menu

    # WEEK 6 UPDATE
    ELSE IF user input is 1:
        GET all orders from orders table
        PRINT orders

    # WEEK 6 UPDATE
    ELSE IF user input is 2:
        # CREATE order

        GET user input for customer name
        GET user input for customer address
        GET user input for customer phone number

        GET all products from products table
        PRINT products
        GET user inputs for comma-separated list of product IDs
        CONVERT above user input to string e.g. "1,3,4"

        GET all couriers from couriers table
        PRINT couriers
        GET user input for courier ID

        SET order status to be 1
        INSERT order into orders table

    # WEEK 6 UPDATE
    ELSE IF user input is 3:
        # UPDATE existing order status

        GET all orders from orders table
        PRINT orders with their IDs

        GET user input for order ID

        GET all order statuses from order_status table
        PRINT order statuses

        GET user input for the updated order status ID

        UPDATE status for the order

    # WEEK 6 UPDATE
    ELSE IF user input is 4:
        # STRETCH - UPDATE existing order

        GET all orders from orders table
        PRINT orders with their IDs
        GET user input for order ID

        GET user input for customer name
        GET user input for customer address
        GET user input for customer phone number

        GET all products from products table
        PRINT products
        GET user inputs for comma-separated list of product IDs
        CONVERT above user input to a string e.g. "2,1,3"

        GET all couriers from couriers table
        PRINT couriers
        GET user input for courier ID

        IF an input is empty, do not update its respective table property
        UPDATE order in orders table

    # WEEK 6 UPDATE
    ELSE IF user input is 4:
        # STRETCH GOAL - DELETE order

        GET all orders from orders table
        PRINT orders with their IDs

        GET user input for order ID
        DELETE order in orders table
```
