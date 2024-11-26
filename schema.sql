-- Create Database
CREATE DATABASE IF NOT EXISTS real_estate_db;
USE real_estate_db;

-- Create Categories table for property types
CREATE TABLE Categories (
   category_id INT PRIMARY KEY AUTO_INCREMENT,
   category_name VARCHAR(50) NOT NULL
);

-- Create Properties table
CREATE TABLE Properties (
   property_id INT PRIMARY KEY AUTO_INCREMENT,
   property_name VARCHAR(255) NOT NULL,
   category_id INT,
   location VARCHAR(100) NOT NULL,
   area_sqft DECIMAL(12,2) NOT NULL,
   year_constructed INT NOT NULL,
   market_value DECIMAL(15,2) NOT NULL,
   FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- Create Transactions table
CREATE TABLE Transactions (
   transaction_id INT PRIMARY KEY AUTO_INCREMENT,
   property_id INT,
   transaction_date DATE NOT NULL,
   transaction_amount DECIMAL(15,2) NOT NULL,
   FOREIGN KEY (property_id) REFERENCES Properties(property_id)
);

-- Create MarketTrends table
CREATE TABLE MarketTrends (
   trend_id INT PRIMARY KEY AUTO_INCREMENT,
   year INT NOT NULL,
   location VARCHAR(100) NOT NULL,
   avg_price_per_sqft DECIMAL(12,2) NOT NULL
);

-- Insert basic categories
INSERT INTO Categories (category_name) VALUES 
('Apartment'),
