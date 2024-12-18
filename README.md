🏘️ Real Estate Data Generator and analytics
Project Overview
A Python-based synthetic data generation tool for creating realistic real estate datasets, focusing on property and market trend analysis.
✨ Key Features

Synthetic Data Generation for Real Estate Properties
MySQL Database Integration
Random Property and Market Trend Data Creation
Basic Data Analytics and Visualization

🛠️ Tech Stack

Language: Python
Database: MySQL
Libraries:

NumPy (Data Generation)
Pandas (Data Manipulation)
Matplotlib (Data Visualization)
mysql-connector-python (Database Connectivity)



📊 Data Generation Details
Property Characteristics

Randomly generated properties across 5 localities:

CIDCO
Garkheda
Samarth Nagar
Kranti Chowk
Bypass Road


Property Attributes:

Unique property names
Random area (500-2500 sq ft)
Construction year (1990-2023)
Market value (5000-15000)



Market Trends

Generates trend data for each locality from 2010-2024
Random average price per square foot (3000-15000)

🚀 Quick Start
Prerequisites

Python 3.7+
MySQL Server
Required Python Packages:
Copypip install mysql-connector-python numpy pandas matplotlib


Setup

Create MySQL database
Update database configuration in db_config
Run the script to generate and insert data

Usage
pythonCopy# Generate properties and market trends
data_generator = RealEstateData()
properties = data_generator.generate_properties()
market_trends = data_generator.generate_market_trends()

# Insert data into database
db = RealEstateDatabase(db_config)
db.insert_data(properties, market_trends)

# Perform analytics
analytics = RealEstateAnalytics()
results = analytics.perform_analytics(properties, market_trends)
📈 Outputs

Property summary statistics
Average market value by location
Yearly average market trends
Matplotlib visualizations:

Property Distribution by Location
Market Trends Over Time
Basic analytics and visualization
Requires manual database setup

🤝 Contributing
Contributions to enhance data generation, add more localities, or improve analytics are welcome!
📄 License
MIT License
