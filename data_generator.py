import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the database configuration 
db_config = {
    'host': 'localhost',          
    'user': 'root',      
    'password': 'YES',  
    'database': 'mysql'   
}

class RealEstateData:
    def __init__(self):
        self.LOCALITIES = ['CIDCO', 'Garkheda', 'Samarth Nagar', 'Kranti Chowk', 'Bypass Road']
    
    def generate_properties(self, num_properties=500):
        return [
            {'property_name': f"Property {i}", 'location': np.random.choice(self.LOCALITIES), 
             'area_sqft': round(np.random.uniform(500, 2500), 2), 'year_constructed': np.random.randint(1990, 2023), 
             'market_value': round(np.random.uniform(5000, 15000), 2)}
            for i in range(num_properties)
        ]

    def generate_market_trends(self):
        return [{'year': year, 'location': location, 'avg_price_per_sqft': round(np.random.uniform(3000, 15000), 2)}
                for year in range(2010, 2024) for location in self.LOCALITIES]

class RealEstateDatabase:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def insert_data(self, properties, market_trends):
        conn = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.executemany("""INSERT INTO Properties (property_name, location, area_sqft, year_constructed, market_value) 
                                  VALUES (%(property_name)s, %(location)s, %(area_sqft)s, %(year_constructed)s, %(market_value)s)""", properties)
            cursor.executemany("""INSERT INTO MarketTrends (year, location, avg_price_per_sqft) 
                                  VALUES (%(year)s, %(location)s, %(avg_price_per_sqft)s)""", market_trends)
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

class RealEstateAnalytics:
    @staticmethod
    def perform_analytics(properties, market_trends):
        # Perform analytics and return data
        property_summary = pd.DataFrame(properties)[['area_sqft', 'market_value']].describe()
        avg_price_by_location = pd.DataFrame(properties).groupby('location')['market_value'].mean()
        yearly_avg_trends = pd.DataFrame(market_trends).groupby('year')['avg_price_per_sqft'].mean()

        # Visualization
        # Property Distribution by Location
        pd.DataFrame(properties)['location'].value_counts().plot(kind='bar', title='Property Distribution by Location')
        plt.xlabel("Location")
        plt.ylabel("Property Count")
        plt.show()

        # Market Trends Over Time
        yearly_avg_trends.plot(title="Market Trends Over Time", ylabel="Avg Price Per Sqft", xlabel="Year")
        plt.show()

        return {
            "property_summary": property_summary,
            "avg_price_by_location": avg_price_by_location,
            "yearly_avg_trends": yearly_avg_trends
        }

if __name__ == "__main__":
    # Generate data
    data_generator = RealEstateData()
    properties = data_generator.generate_properties()
    market_trends = data_generator.generate_market_trends()

    # Insert data into SQL
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'YES',
        'database': 'mysql'
    }
    db = RealEstateDatabase(db_config)
    db.insert_data(properties, market_trends)

    # Perform Analytics
    analytics = RealEstateAnalytics()
    results = analytics.perform_analytics(properties, market_trends)

    # Print the analytics results
    print("\nProperty Summary Statistics:")
    print(results["property_summary"])

    print("\nAverage Market Value by Location:")
    print(results["avg_price_by_location"])

    print("\nYearly Average Market Trends:")
    print(results["yearly_avg_trends"])
