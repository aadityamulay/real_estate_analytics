-- Create Categories table for property types (apartments, houses, etc.)
CREATE TABLE Categories (
   category_id INT PRIMARY KEY AUTO_INCREMENT,
   category_name VARCHAR(50) NOT NULL
);

-- Create Properties table
CREATE TABLE Properties (
   property_id INT PRIMARY KEY AUTO_INCREMENT,
   property_name VARCHAR(255) NOT NULL,  -- Increased from 100 to 255
   category_id INT,
   location VARCHAR(100) NOT NULL,
   area_sqft DECIMAL(12,2) NOT NULL,     -- Increased precision from 10,2 to 12,2
   year_constructed INT NOT NULL,
   market_value DECIMAL(15,2) NOT NULL,  -- Increased precision from 12,2 to 15,2
   FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- Create Transactions table
CREATE TABLE Transactions (
   transaction_id INT PRIMARY KEY AUTO_INCREMENT,
   property_id INT,
   transaction_date DATE NOT NULL,
   transaction_amount DECIMAL(15,2) NOT NULL,  -- Increased precision from 12,2 to 15,2
   FOREIGN KEY (property_id) REFERENCES Properties(property_id)
);

-- Create MarketTrends table
CREATE TABLE MarketTrends (
   trend_id INT PRIMARY KEY AUTO_INCREMENT,
   year INT NOT NULL,
   location VARCHAR(100) NOT NULL,
   avg_price_per_sqft DECIMAL(12,2) NOT NULL  -- Increased precision from 10,2 to 12,2
);

-- Insert basic categories
INSERT INTO Categories (category_name) VALUES 
('Apartment'),
('House');