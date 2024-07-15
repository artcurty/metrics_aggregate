from concurrent.futures import ThreadPoolExecutor, as_completed 
from output_adapters.csv_adapter import CsvFileCreator
from output_adapters.http_client import HttpClient
import logging

class MetricsService:
    def __init__(self, output_port: CsvFileCreator, api_client: HttpClient, api_configs: list[dict]):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.output_port = output_port
        self.api_client = api_client
        self.api_configs = api_configs

    def get_api_config(self, team: str, start_date_iso: str, end_date_iso: str) -> list[dict]:
        api_configs = []

        for api in self.api_configs:
            api_config = {
                'name': api['name'],
                'method': api['method'],
                'url': api['url'],
                'headers': api['headers']
            }
            
            params = api.get('parameters')
            if params:
                api_config['params'] = {k: v.format(team=team, start_date=start_date_iso, end_date=end_date_iso) for k, v in params.items()}
            
            body = api.get('body')
            if body:
                api_config['body'] = {k: v.format(team=team, start_date=start_date_iso, end_date=end_date_iso) for k, v in body.items()}
            
            api_configs.append(api_config)
        
        return api_configs

    def fetch_metrics(self, team_name: str, start_date: str, end_date: str) -> dict:
        apis_config = self.get_api_config(team_name, start_date, end_date)
        results = {}
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.api_client.fetch_data, config): config['name'] for config in apis_config}
            for future in as_completed(futures):
                name = futures[future]
                try:
                    results[name] = future.result()
                except Exception as e:
                    results[name] = 'ERROR'

        filename = self.output_port.create_file(start_date, end_date, team_name, results, self.api_configs)
        return results, filename
