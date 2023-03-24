# Web Health Check API - Google Cloud Function

A simple Google Cloud Function for checking the health of websites, servers, and services using port checks, ping, or HTTP requests.

## Dependencies

- Python 3.6+
- Functions Framework for Python
- Flask
- Requests
- ping3

## Usage
This function can be used to perform the following health checks:

- Port checks
- Ping checks
- Website checks

To perform a health check, make a POST request to the function with the required fields in the form data.

### Required fields
- `type`: Type of health check to perform. Can be one of port, ping, or website.
- `target`: The target URL or IP address.
- `port`: The port to use for the port check.
- `settings`: A JSON string containing additional settings for the health check.

### Settings
The settings field should contain a JSON string with the following keys:

- `timeout_seconds`: Timeout duration in seconds for the check.
- `request_basic_auth_username` (optional): Basic authentication username, required for website checks that need authentication.
- `request_basic_auth_password` (optional): Basic authentication password, required for website checks that need authentication.
- `request_method` (optional): HTTP method to use for the website check. Defaults to 'GET'. Can be one of 'GET', 'POST', 'PUT', 'PATCH', or 'DELETE'.
- `request_headers` (optional): A list of dictionaries containing header names and values for the website check.
- `request_bod`y (optional): The request body for POST, PUT, and PATCH methods in the website check.
- `response_status_code` (optional): Expected HTTP status code for the website check.
- `response_body` (optional): Expected substring in the response body for the website check.
- `response_headers` (optional): A list of dictionaries containing expected header names and values in the response for the website check.

### Example Request
```
import requests

data = {
    'type': 'website',
    'target': 'https://example.com',
    'port': 80,
    'settings': json.dumps({
        'timeout_seconds': 5,
        'request_method': 'GET',
        'response_status_code': 200
    })
}

response = requests.post("http://localhost:8080", data=data)
print(response.json())
```

### Example Response
Response
The function returns a JSON object with the following keys:

```{"is_ok":0,"response_time":0,"response_status_code":0,"error":null}```

## Local Deployment
To deploy the function using Functions Framework, run the following command:

```functions-framework --target=web_health_check --port=8080```

The function will be accessible at http://localhost:8080.

## Deploy to Google Cloud Platform
