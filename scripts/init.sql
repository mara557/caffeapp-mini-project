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

-- Create orders table
CREATE TABLE orders (
  id INT NOT NULL AUTO_INCREMENT,
  customer_name VARCHAR(255) NOT NULL,
  customer_address VARCHAR(255) NOT NULL,
  customer_phone VARCHAR(20) NOT NULL,
  courier INT NOT NULL,
  status INT NOT NULL,
  items VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (courier) REFERENCES couriers(id),
  FOREIGN KEY (status) REFERENCES order_status(id)
);

-- Insert default order statuses
INSERT INTO order_status (order_status) VALUES ('PREPARING'), ('READY'), ('DELIVERED');
