# Metrics Aggregator

The **Metrics Aggregator** is a project that collects metrics from various APIs and generates reports based on this data. The project uses Flask to build an API that allows requesting metrics within a date range and for a specific team.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Usage](#usage)

## Overview

This project is an API that allows the collection and aggregation of metrics from various external APIs. It is designed to be easy to configure and extend. The collected data can be stored in CSV files and accessed via a REST API.

## Features

- **Metrics Collection:** Aggregates data from multiple external APIs.
- **Report Generation:** Creates CSV files with the collected data.
- **RESTful API:** Allows requesting metrics based on date parameters and team name.

## Prerequisites

- **Python 3.8+**
- **Python Libraries:** Required libraries are listed in `requirements.txt`.

## Environment Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/metrics_aggregator.git
   cd metrics_aggregator
   ```

2. **Install Libraries:**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```bash
metrics_aggregator/
│
├── app/
│   ├── app.py           # Main file to create and configure the Flask app
│   ├── core/
│   │   ├── services.py  # Implements the business logic for metrics service
│   ├── output_adapters/
│   │   ├── csv_adapter.py             # Adapter for creating CSV files
│   ├── input_adapters/
│   │   ├── http_controller_adapter.py # controller to manage API requests
├── config.json                        # JSON configuration file
├── requirements.txt                   # Project dependencies
└── README.md                          # Project documentation
```

## Usage

#### Configuration File Fields

This table explains each possible field in the `config.json` file used to configure API requests for the Metrics Aggregator project.

| Field        | Type   | Description                                                              | Example                                                                    |
| ------------ | ------ | ------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| `name`       | String | The name of metric.                                                      | `"metrica 1"`                                                              |
| `method`     | String | The HTTP method used for the API request.                                | `"GET", "POST"`                                                            |
| `url`        | String | The endpoint URL of the API where the request will be sent.              | `"https://{nome_organização}.atlassian.net"`                               |
| `headers`    | Object | A dictionary of HTTP headers to include in the request.                  | `{"Authorization": "Bearer your_api_token"}`                               |
| `parameters` | Object | A dictionary of query parameters to be included in the URL for requests. | `{"team": "{team}", "startDate": "{start_date}", "endDate": "{end_date}"}` |
| `body`       | Object | A dictionary representing the JSON body to be included in POST requests. | `{"team": "{team}", "startDate": "{start_date}", "endDate": "{end_date}"}` |

#### Example `config.json` File

```json
{
  "apis": [
    {
      "name": "metrica 1",
      "method": "GET",
      "url": "https://my-metric-url.com",
      "headers": {
        "Authorization": "Bearer your_api_token"
      },
      "parameters": {
        "team": "{team}",
        "startDate": "{start_date}",
        "endDate": "{end_date}"
      }
    },
    {
      "name": "metrica 2",
      "method": "POST",
      "url": "https://my-metric-url.com",
      "headers": {
        "Authorization": "Bearer your_api_token"
      },
      "body": {
        "team": "{team}",
        "startDate": "{start_date}",
        "endDate": "{end_date}"
      }
    }
  ]
}
```

#### Start the Flask Server

```bash
python app/app.py
```

#### API Documentation

The API documentation is available at {host}/docs (Ex: http://localhost:5000/docs). Use this URL to explore the API and view the endpoints and their parameters.

##### Make a Request to Get Metrics

```bash
curl "http://localhost:5000/metrics?startDate=2024-01-01&endDate=2024-01-31&team=example_team"
```

#### Receive the Report

The server will return a JSON with the collected metrics and the name of the generated CSV file.
