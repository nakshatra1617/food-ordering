CREATE DATABASE food_ordering;
USE food_ordering;
SHOW TABLES;

CREATE TABLE restaurants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(15),
    cuisine_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50),        -- e.g. "Starter", "Main", "Dessert"
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
);

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    status ENUM('pending', 'confirmed', 'preparing', 'delivered', 'cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price_at_order DECIMAL(10, 2) NOT NULL,   -- price snapshot when order was placed
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

INSERT INTO restaurants (name, address, phone, cuisine_type) VALUES
('Pizza Palace', '123 Main Street', '9876543210', 'Italian'),
('Burger Barn', '456 Oak Avenue', '9123456780', 'American'),
('Spice Garden', '789 Elm Road', '9012345678', 'Indian');

INSERT INTO menu_items (restaurant_id, name, description, price, category) VALUES
(1, 'Margherita Pizza', 'Classic cheese and tomato pizza', 12.99, 'Main'),
(1, 'Garlic Bread', 'Toasted bread with garlic butter', 4.99, 'Starter'),
(1, 'Tiramisu', 'Classic Italian dessert', 6.99, 'Dessert'),
(2, 'Classic Burger', 'Beef patty with lettuce and cheese', 9.99, 'Main'),
(2, 'Fries', 'Crispy golden fries', 3.99, 'Starter'),
(2, 'Chocolate Shake', 'Thick chocolate milkshake', 4.99, 'Drinks'),
(3, 'Butter Chicken', 'Creamy tomato chicken curry', 13.99, 'Main'),
(3, 'Naan', 'Soft Indian flatbread', 2.99, 'Starter'),
(3, 'Gulab Jamun', 'Sweet milk dumplings in syrup', 4.99, 'Dessert');

INSERT INTO customers (name, email, phone, address) VALUES
('John Doe', 'john@example.com', '9999999999', '10 Park Lane');

SELECT * FROM restaurants;

USE food_ordering;

INSERT INTO customers (name, email, phone, address) VALUES
('Nakshatra Shinde', 'nakshatra@example.com', '9876543210', 'Pune, Maharashtra'),
('Rahul Sharma', 'rahul.sharma@example.com', '9812345678', 'Mumbai, Maharashtra'),
('Priya Patel', 'priya.patel@example.com', '9823456789', 'Ahmedabad, Gujarat'),
('Arjun Mehta', 'arjun.mehta@example.com', '9834567890', 'Delhi, India'),
('Sneha Kulkarni', 'sneha.kulkarni@example.com', '9845678901', 'Nashik, Maharashtra'),
('Vikram Singh', 'vikram.singh@example.com', '9856789012', 'Jaipur, Rajasthan'),
('Anjali Desai', 'anjali.desai@example.com', '9867890123', 'Surat, Gujarat'),
('Rohan Joshi', 'rohan.joshi@example.com', '9878901234', 'Bangalore, Karnataka'),
('Pooja Nair', 'pooja.nair@example.com', '9889012345', 'Chennai, Tamil Nadu'),
('Amit Verma', 'amit.verma@example.com', '9890123456', 'Hyderabad, Telangana');

SELECT * FROM customers;

USE food_ordering;
ALTER TABLE customers ADD COLUMN password VARCHAR(255) DEFAULT NULL;