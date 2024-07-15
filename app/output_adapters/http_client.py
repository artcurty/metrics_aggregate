import requests
import logging

class HttpClient:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def fetch_data(self, config: dict) -> dict:
        try:
            response = requests.request(
                method=config['method'],
                url=config['url'],
                headers=config.get('headers', {}),
                params=config.get('params', {}),
                json=config.get('json', {}),
                data=config.get('data', {})
            )
            jsonResponse = response.json()

            logging.info(f"Request executed for: {config['name']} with result success: {jsonResponse}")

            return jsonResponse
        except requests.RequestException as e:
            logging.error(f"Request executed for: {config['name']} with result error: {str(e)}")
            return {'error': 'ERROR'}
