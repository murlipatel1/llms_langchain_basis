-- Create a new database
CREATE DATABASE IF NOT EXISTS llm_bd;
USE llm_db;

-- Create `customers` table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    join_date DATE
);

-- Create `purchases` table
CREATE TABLE IF NOT EXISTS purchases (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    purchase_date DATE,
    amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create `products` table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2),
    stock_quantity INT
);

-- Create `sales` table
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    sale_date DATE,
    amount DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert sample data into `customers` table
INSERT INTO customers (name, email, join_date)
VALUES 
    ('Alice Johnson', 'alice@example.com', '2024-01-10'),
    ('Bob Smith', 'bob@example.com', '2024-02-15'),
    ('Carol Williams', 'carol@example.com', '2024-03-20');

-- Insert sample data into `products` table
INSERT INTO products (product_name, price, stock_quantity)
VALUES 
    ('Laptop', 1200.00, 5),
    ('Headphones', 150.00, 25),
    ('Keyboard', 75.00, 40);

-- Insert sample data into `purchases` table
INSERT INTO purchases (customer_id, product_id, purchase_date, amount)
VALUES 
    (1, 1, '2024-07-05', 1200.00),
    (2, 2, '2024-07-10', 150.00),
    (3, 3, '2024-07-15', 75.00),
    (1, 2, '2024-07-20', 150.00);

-- Insert sample data into `sales` table
INSERT INTO sales (product_id, sale_date, amount)
VALUES 
    (1, '2024-06-15', 1200.00),
    (2, '2024-07-01', 150.00),
    (3, '2024-07-05', 75.00),
    (1, '2024-07-10', 1200.00);
