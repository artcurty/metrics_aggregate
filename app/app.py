from flask import Flask
from flasgger import Swagger
from core.services import MetricsService
from output_adapters.http_client import HttpClient
from output_adapters.csv_adapter import CsvFileCreator
from input_adapters.http_controller_adapter import create_metrics
import json
import os

app = Flask(__name__) 
swagger_config = {
    "info": {
        "title": "My API",
        "description": "This is a sample API",
        "version": "1.0.0"
    },
    "schemes": [
        "http"
    ]
}

swagger = Swagger(app, template=swagger_config)

def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as config_file:
        return json.load(config_file)
    
def create_app(config: dict) -> Flask:
    output_port = CsvFileCreator()
    api_client = HttpClient()
    metrics_service = MetricsService(output_port, api_client, config['apis'])
    metrics_blueprint = create_metrics(metrics_service)
    app.register_blueprint(metrics_blueprint)

    return app

if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), '../config.json')
    config = load_config(config_path)
    app = create_app(config)
    app.run(port=5000, debug=True)
