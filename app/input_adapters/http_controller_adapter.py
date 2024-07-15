from flask import request, jsonify, Blueprint
from flasgger import swag_from
from core.services import MetricsService
from core.utils import to_iso_utc
import logging

class MetricsController:

    def __init__(self, metrics_service: MetricsService):
        self.metrics_service = metrics_service
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_metrics(self):
        logging.info("Start get metrics")
        
        start_date = request.args.get('startDate', '')
        end_date = request.args.get('endDate', '')
        team_name = request.args.get('team', '')

        if not start_date or not end_date or not team_name:
            return jsonify({'error': 'Missing required parameters'}), 400

        try:
            start_date_iso = to_iso_utc(date_str=start_date)
            end_date_iso = to_iso_utc(date_str=end_date, is_end_date=True)
            
            results, filename = self.metrics_service.fetch_metrics(start_date_iso, end_date_iso, team_name)
            logging.info("Finish get metrics")

            return jsonify({'message': 'Metrics fetched successfully', 'results': results, 'file': filename})
        except Exception as e:
            logging.error({'error': 'Failed to fetch metrics', 'details': str(e)})
            return jsonify({'error': 'Failed to fetch metrics', 'details': str(e)}), 500
    
def create_metrics(metrics_service: MetricsService) -> Blueprint:
    controller = MetricsController(metrics_service)
    blueprint = Blueprint('metrics', __name__)

    @swag_from({
        'tags': ['Metrics'],
        'description': 'Fetch metrics for a specific team within a date range',
        'parameters': [
            {
                'name': 'startDate',
                'in': 'query',
                'type': 'string',
                'format': 'date',
                'required': True,
                'description': 'Start date for metrics retrieval',
                'example': '2024-05-01'
            },
            {
                'name': 'endDate',
                'in': 'query',
                'type': 'string',
                'format': 'date',
                'required': True,
                'description': 'End date for metrics retrieval',
                'example': '2024-05-31'
            },
            {
                'name': 'team',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Name of the team for metrics retrieval',
                'example': 'my'
            }
        ],
        'responses': {
            '200': {
                'description': 'Metrics successfully fetched',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string'
                        },
                        'results': {
                            'type': 'object',
                            'additionalProperties': True
                        },
                        'file': {
                            'type': 'string'
                        }
                    }
                }
            },
            '400': {
                'description': 'Missing required parameters'
            },
            '500': {
                'description': 'Failed to fetch metrics'
            }
        }
    })
    @blueprint.route('/metrics', methods=['POST'])
    def get_metrics():
        return controller.get_metrics()

    return blueprint