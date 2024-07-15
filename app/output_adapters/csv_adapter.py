
import os
import logging
import csv

class CsvFileCreator:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def get_csv_headers(self, api_configs: list[dict]) -> list[str]:
        return ['data inicio', 'data fim', 'time'] + [api['name'] for api in api_configs]

    def sanitize_filename(self, filename: str) -> str:
        return filename.replace(":", "_")

    def create_file(self, start_date: str, end_date: str, team_name: str, results: dict, api_configs: list[dict]) -> str:
        directory = os.path.join(os.getcwd(), 'reports')

        if not os.path.exists(directory):
            os.makedirs(directory)
        
        headers = self.get_csv_headers(api_configs)
        filename = self.sanitize_filename(f"metrics_{team_name}_{start_date}_to_{end_date}.csv")
        file_path = os.path.join(directory, filename)
        
        row = [start_date, end_date, team_name] + [results.get(header, 'ERROR') for header in headers[3:]]
        
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerow(row)
            logging.info(f"Arquivo salvo em: {file_path}")
        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo: {e}")
        
        return file_path 