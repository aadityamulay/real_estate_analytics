import mysql.connector
import numpy as np
from faker import Faker
import logging
import pandas as pd
from config import ConfigManager

class RealEstateDataGenerator:
    def __init__(self, config=None):
        self.fake = Faker('en_IN')
        self.config = config or ConfigManager.load_config()
        self.LOCALITIES = [
            'CIDCO', 'Garkheda', 'Samarth Nagar', 
            'Kranti Chowk', 'Bypass Road'
        ]
        self._setup_logging()

    def _setup_logging(self):
        log_config = ConfigManager.get_logging_config()
        logging.basicConfig(
            level=getattr(logging, log_config['level']),
            format=log_config['format'],
            filename=log_config['filename']
        )

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
        return [
            {
                'property_id': np.random.randint(1, 501),
                'transaction_date': self.fake.date_between(start_date='-5y', end_date='today'),
                'transaction_amount': round(np.random.uniform(1000000, 10000000), 2)
            } for _ in range(num_transactions)
        ]

    def generate_market_trends(self):
        return [
            {
                'year': year,
                'location': location,
                'avg_price_per_sqft': round(np.random.uniform(3000, 15000), 2)
            } for year in range(2010, 2024)
            for location in self.LOCALITIES
        ]

    def insert_data(self):
        try:
            conn = mysql.connector.connect(**self.config['database'])
            cursor = conn.cursor(dictionary=True)

            # Properties Insertion
            properties = self.clean_properties(self.generate_properties())
            cursor.executemany("""
                INSERT INTO Properties 
                (property_name, category_id, location, area_sqft, year_constructed, market_value)
                VALUES (%(property_name)s, %(category_id)s, %(location)s, %(area_sqft)s, %(year_constructed)s, %(market_value)s)
            """, properties)
            conn.commit()

            # Transactions Insertion
            transactions = self.generate_transactions()
            cursor.executemany("""
                INSERT INTO Transactions 
                (property_id, transaction_date, transaction_amount)
                VALUES (%(property_id)s, %(transaction_date)s, %(transaction_amount)s)
            """, transactions)
            conn.commit()

            # Market Trends Insertion
            market_trends = self.generate_market_trends()
            cursor.executemany("""
                INSERT INTO MarketTrends 
                (year, location, avg_price_per_sqft)
                VALUES (%(year)s, %(location)s, %(avg_price_per_sqft)s)
            """, market_trends)
            conn.commit()

            logging.info(f"Successfully processed {len(properties)} properties, {len(transactions)} transactions, and market trends.")
            conn.close()
        except mysql.connector.Error as err:
            logging.error(f"Database Error: {err}")
        except Exception as e:
            logging.error(f"Unexpected Error: {e}")

def main():
    try:
        generator = RealEstateDataGenerator()
        generator.insert_data()
        print("Data generation completed successfully!")
    except Exception as e:
        print(f"Error in data generation: {e}")

if __name__ == "__main__":
    main()
