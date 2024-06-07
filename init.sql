DROP DATABASE IF EXISTS cafe_db;
CREATE DATABASE cafe_db;

USE cafe_db;

-- Create products table
CREATE TABLE products (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(5, 2) NOT NULL,
  PRIMARY KEY (id)
);

-- Create couriers table
CREATE TABLE couriers (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  PRIMARY KEY (id)
);

-- Create order_status table
CREATE TABLE order_status (
  id INT NOT NULL AUTO_INCREMENT,
  order_status VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);

-- Create customers table
CREATE TABLE customers (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  address VARCHAR(255) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  PRIMARY KEY (id)
);

-- Create orders table
CREATE TABLE orders (
  id INT NOT NULL AUTO_INCREMENT,
  customer_id INT NOT NULL,
  courier INT NOT NULL,
  status INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  FOREIGN KEY (courier) REFERENCES couriers(id),
  FOREIGN KEY (status) REFERENCES order_status(id)
);

-- Create order_items table for many-to-many relationship between orders and products
CREATE TABLE order_items (
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert default order statuses
INSERT INTO order_status (order_status) VALUES ('PREPARING'), ('READY'), ('DELIVERED');