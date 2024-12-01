import numpy as np
from faker import Faker
import pandas as pd
import logging
from config import ConfigManager
import mysql.connector
import matplotlib.pyplot as plt

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename=ConfigManager.get_logging_config()['filename']
)

class RealEstateDataGenerator:
    def __init__(self):
        self.fake = Faker('en_IN')
        self.config = ConfigManager.load_config()
        self.LOCALITIES = ['CIDCO', 'Garkheda', 'Samarth Nagar', 'Kranti Chowk', 'Bypass Road']

    def generate_properties(self, num_properties=500):
        return [
            {
                'property_name': f"{self.fake.company()} Property",
                'category_id': np.random.choice([1, 2]),
                'location': np.random.choice(self.LOCALITIES),
                'area_sqft': (area := round(np.random.uniform(500, 2500), 2)),
                'year_constructed': (year := np.random.randint(1990, 2023)),
                'market_value': area * np.random.uniform(5000, 15000)
            } for _ in range(num_properties)
        ]

    def clean_properties(self, properties):
        df = pd.DataFrame(properties)
        df = df[(df['area_sqft'] > 0) & (df['market_value'] > 0)]
        return df.to_dict('records')

    def generate_transactions(self, num_transactions=100):
        """Generates dummy transaction data for properties."""
        return [
            {
                'property_id': np.random.randint(1, 501),
                'transaction_date': self.fake.date_between(start_date='-5y', end_date='today'),
                'transaction_amount': round(np.random.uniform(1000000, 10000000), 2)
            }
            for _ in range(num_transactions)
        ]

    def generate_market_trends(self):
        """Generates dummy market trend data."""
        return [
            {
                'year': year,
                'location': location,
                'avg_price_per_sqft': round(np.random.uniform(3000, 15000), 2)
            }
            for year in range(2010, 2024)
            for location in self.LOCALITIES
        ]

    def insert_data(self):
        try:
            conn = mysql.connector.connect(**self.config['database'])
            cursor = conn.cursor(dictionary=True)

            # Generate, clean, and insert properties
            properties = self.clean_properties(self.generate_properties())
            cursor.executemany("""
                INSERT INTO Properties 
                (property_name, category_id, location, area_sqft, year_constructed, market_value)
                VALUES (%(property_name)s, %(category_id)s, %(location)s, %(area_sqft)s, %(year_constructed)s, %(market_value)s)
            """, properties)
            conn.commit()

            # Generate and insert transactions
            transactions = self.generate_transactions()
            cursor.executemany("""
                INSERT INTO Transactions 
                (property_id, transaction_date, transaction_amount)
                VALUES (%(property_id)s, %(transaction_date)s, %(transaction_amount)s)
            """, transactions)
            conn.commit()

            # Generate and insert market trends
            market_trends = self.generate_market_trends()
            cursor.executemany("""
                INSERT INTO MarketTrends 
                (year, location, avg_price_per_sqft)
                VALUES (%(year)s, %(location)s, %(avg_price_per_sqft)s)
            """, market_trends)
            conn.commit()

            logging.info(f"Successfully processed {len(properties)} properties, {len(transactions)} transactions, and market trends.")
            conn.close()

            # Visualization
            self.visualize_data()

        except mysql.connector.Error as err:
            logging.error(f"Database Error: {err}")
        except Exception as e:
            logging.error(f"Unexpected Error: {e}")

    def visualize_data(self):
        gen = RealEstateDataGenerator()

        # Market Trends
        trends = pd.DataFrame(gen.generate_market_trends())
        trends.groupby(['year', 'location'])['avg_price_per_sqft'].mean().unstack().plot(title="Market Trends")
        plt.xlabel("Year"); plt.ylabel("Avg Price/Sqft"); plt.show()

        # Property Distribution
        pd.DataFrame(gen.generate_properties())['location'].value_counts().plot(kind='bar', title="Property Distribution")
        plt.xlabel("Location"); plt.ylabel("Count"); plt.show()

        # Transaction Amounts
        pd.DataFrame(gen.generate_transactions())['transaction_amount'].plot(kind='hist', bins=10, title="Transaction Amounts", color='orange', edgecolor='black')
        plt.xlabel("Amount"); plt.ylabel("Frequency"); plt.show()

if __name__ == "__main__":
    RealEstateDataGenerator().insert_data()
