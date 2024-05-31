# Mini Project Week 5

CSV is great, but there is a better option. Let's store our couriers and products in a database, we'll leave orders as they are for now.

An order's courier and product items properties currently use indexes to reference these entities, we're going to change this to use ids instead.

Remember to update unit-tests.

## Goals

As a user I want to:

- create a product or courier and add it to a database table
- create an order and add the order dictionary to a list
- view all products, couriers, or orders
- update the status of an order
- persist my data
- _STRETCH_ update or delete a product, order, or courier
- _BONUS_ list orders by status or courier
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

- An `order` should be a `dict`, i.e:

```json
{
  "customer_name": "John",
  "customer_address": "Unit 2, 12 Main Street, LONDON, WH1 2ER",
  "customer_phone": "0789887334",
  "courier": 2, // Courier ID
  "status": "preparing",
  "items": "1, 3, 4" // Product IDs
}
```

- Orders should be persisted to a `.csv` file on a new line for each `order`, ie:

```csv
# ORDER
John,"Unit 2, 12 Main Street, LONDON, WH1 2ER",2,preparing,"1,3,4"
```

## Pseudo Code

```txt
# we are no longer reading products and couriers from files
# we are now reading product and courier data from database tables

LOAD orders from orders.csv
CREATE order status list

PRINT main menu options
GET user input for main menu option

IF user input is 0:
    SAVE orders to order.csv
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

    ELSE IF user input is 1:
        PRINT orders dictionary

    ELSE IF user input is 2:
        GET user input for customer name
        GET user input for customer address
        GET user input for customer phone number

        # WEEK 5 UPDATE
        GET all products from products table
        PRINT products
        GET user inputs for comma-separated list of product IDs
        CONVERT above user input to a string e.g. "2,1,3"

        # WEEK 5 UPDATE
        GET all couriers from couriers table
        PRINT couriers
        GET user input for courier ID

        SET order status to be 'PREPARING'

        CREATE new order dictionary with above properties
        APPEND order to orders list

    ELSE IF user input is 3:
        # UPDATE existing order status

        PRINT orders list with its index values
        GET user input for order index value

        PRINT order status list with index values
        GET user input for order status index value
        UPDATE status for order

    ELSE IF user input is 4:
        # STRETCH - UPDATE existing order

        PRINT orders list with its index values
        GET user input for order index value

        FOR EACH key-value pair in selected order dictionary:
            GET user input for updated property
            IF user input is blank:
                do not update this property
            ELSE:
                update the property value with user input

    ELSE IF user input is 5:
        # STRETCH GOAL - DELETE order
                    
        PRINT orders list
        GET user input for order index value
        DELETE order at index in order list
```
