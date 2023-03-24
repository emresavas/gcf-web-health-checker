import functions_framework
import json
import requests
from flask import request, jsonify
from ping3 import ping
import socket
import time

@functions_framework.http
def web_health_check(request):
    if request.method == 'GET':
        return 'only post'

    # Potential error checks
    if not request.form:
        return 'no form'

    required = ['type', 'target', 'port', 'settings']

    for required_field in required:
        if required_field not in request.form:
            return 'no required fields'

    settings = json.loads(request.form['settings'])

    error = None

    if request.form['type'] == 'port':
        # Port
        target = request.form['target']
        timeout_seconds = settings['timeout_seconds']
        port = int(request.form['port'])

        start_time = time.monotonic()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout_seconds)
                s.connect((target, port))
                response_time = (time.monotonic() - start_time) * 1000
                response_status_code = 0
                is_ok = 1
        except:
            response_time = 0
            is_ok = 0
            response_status_code = 0

    elif request.form['type'] == 'ping':
        # Ping check
        latency = ping(request.form['target'], timeout=settings['timeout_seconds'], unit='ms', size=32)

        if latency is not None:
            response_status_code = 0
            response_time = latency

            is_ok = 1
        else:
            response_status_code = 0
            response_time = 0

            is_ok = 0

    elif request.form['type'] == 'website':
        # Website check
        try:
            # Set auth
            auth = (settings['request_basic_auth_username'], settings['request_basic_auth_password'])

            # Make the request to the website
            method = settings['request_method'].lower()
            headers = {header['name']: header['value'] for header in settings['request_headers']}

            if method in ['post', 'put', 'patch']:
                response = requests.request(method, request.form['target'], headers=headers, auth=auth, data=settings['request_body'])
            else:
                response = requests.request(method, request.form['target'], headers=headers, auth=auth)

            response_status_code = response.status_code
            response_time = response.elapsed.total_seconds() * 1000

            is_ok = 1

            if response_status_code != settings['response_status_code']:
                is_ok = 0
                error = {'type': 'response_status_code'}

            if settings['response_body'] and settings['response_body'] not in response.text:
                is_ok = 0
                error = {'type': 'response_body'}

            for response_header in settings['response_headers']:
                response_header_name = response_header['name'].lower()

                if response_header_name not in response.headers or (response.headers[response_header_name] != response_header['value']):
                    is_ok = 0
                    error = {'type': 'response_header'}
                    break

        except Exception as exception:
            response_status_code = 0
            response_time = 0
            error = {
                'type': 'exception',
                'code': 0,
                'message': str(exception),
            }

            is_ok = 0

    response = {
        'is_ok': is_ok,
        'response_time': response_time,
        'response_status_code': response_status_code,
        'error': error,
    }

    return jsonify(response)
