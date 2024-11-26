import os

class ConfigManager:
    @staticmethod
    def load_config():
        return {
            'database': {
                'host': os.getenv('DB_HOST', 'localhost'),
                'user': os.getenv('DB_USER', 'your_username'),
                'password': os.getenv('DB_PASSWORD', 'your_password'),
                'database': os.getenv('DB_NAME', 'real_estate_db')
            }
        }

    @staticmethod
    def get_logging_config():
        return {
            'level': 'INFO',
            'format': '%(asctime)s - %(levelname)s: %(message)s',
            'filename': 'real_estate_data_generation.log'
        }
