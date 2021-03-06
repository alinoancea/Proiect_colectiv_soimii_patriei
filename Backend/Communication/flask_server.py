import json
import logging

from flask import Flask, request
from flask_socketio import SocketIO

from Controller.controller import Controller


class FlaskServer:
    flask_app = Flask(__name__)
    app = SocketIO(flask_app)

    def __init__(self, config_data, controller: Controller):
        self.controller = controller
        self.host = config_data["flask_host"]
        self.port = config_data["flask_port"]
        self.request_data = {}
        self.require_token = ('/api/logout', '/profile', '/api/edit_profile', '/job/', '/api/request_job',
                              '/api/add_job', '/api/jobs', '/api/applicants')
        self.logger = logging.getLogger()

        self.init_requests()

    def run(self):
        self.app.run(self.flask_app, self.host, self.port)

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def stop(self):
        self.shutdown_server()

    def init_requests(self):
        self.flask_app.add_url_rule('/test', 'test_request', self.test_request, methods=['GET', 'POST'])
        self.flask_app.add_url_rule('/api/register', 'register', self.register, methods=['POST'])
        self.flask_app.add_url_rule('/api/login', 'login', self.login, methods=['POST'])
        self.flask_app.add_url_rule('/activation/<key>', 'activation/<key>', self.activation, methods=['GET'])
        self.flask_app.add_url_rule('/job/<job_id>', 'job/<job_id>', self.get_job_details, methods=['POST'])
        self.flask_app.add_url_rule('/api/request_job', 'request_job', self.request_job, methods=['POST'])
        self.flask_app.add_url_rule('/api/add_job', 'add_job', self.add_job, methods=['POST'])
        self.flask_app.add_url_rule('/api/logout', 'logout', self.logout, methods=['POST'])

        self.flask_app.add_url_rule('/api/filter', 'filter', self.filter, methods=['POST'])

        self.flask_app.add_url_rule('/profile', 'profile', self.profile, methods=['POST'])
        self.flask_app.add_url_rule('/api/edit_profile', 'edit_profile', self.edit_profile, methods=['POST'])
        self.flask_app.add_url_rule('/api/jobs', 'jobs', self.jobs, methods=['POST'])
        self.flask_app.add_url_rule('/api/jobs_for_provider', 'jobs_for_provider', self.jobs_for_provider, methods=['POST'])
        self.flask_app.add_url_rule('/api/applicants', 'applicants', self.applicants, methods=['POST'])
        self.flask_app.add_url_rule('/api/get_job_types', 'get_job_types', self.get_job_types, methods=['POST'])
        self.flask_app.before_request(self.verify_user_token)

    def test_request(self):
        self.request_data = request.get_json()
        self.logger.debug("Req data: {}".format(self.request_data))
        return json.dumps("Hello world! Got req: {}".format(self.request_data))

    def get_job_types(self):
        status, response = self.controller.get_job_types()
        return json.dumps({'status': status, 'response': response})

    def register(self):
        request_data = request.get_json() or {}
        status, response = self.controller.register(request_data)
        return json.dumps({'status': status, 'response': response})

    def login(self):
        request_data = request.get_json() or {}
        status, response = self.controller.login(request_data)
        return json.dumps({'status': status, 'response': response})

    def activation(self, key):
        return self.controller.activate(key)

    def get_job_details(self, job_id):
        status, response = self.controller.get_job(job_id)
        return json.dumps({'status': status, 'response': response})

    def request_job(self):
        request_data = request.get_json() or {}
        status = -1
        response = '[!] Give some parameters!'
        if request_data:
            status, response = self.controller.request_job(request_data)

        return json.dumps({'status': status, 'response': response})

    def add_job(self):
        request_data = request.get_json() or {}
        status, response = self.controller.add_job(request_data)

        return json.dumps({'status': status, 'response': response})

    def logout(self):
        request_data = request.get_json() or {}
        status, response = self.controller.logout(request_data)
        return json.dumps({'status': status, 'response': response})

    def profile(self):
        request_data = request.get_json() or {}
        status, response = self.controller.profile(request_data)
        return json.dumps({'status': status, 'response': response})

    def edit_profile(self):
        request_data = request.get_json() or {}
        status, response = self.controller.edit_profile(request_data)

        return json.dumps({'status': status, 'response': response})

    def verify_user_token(self):
        json_data = request.get_json()
        req_path = request.path

        if not req_path.startswith('/activation/'):

            if req_path.startswith('/job/'):
                req_path = '/job/'

            if req_path in self.require_token:
                if not json_data or 'token' not in json_data:
                    return json.dumps({'status': -1, 'response': 'Token required!'})
                elif not self.controller.token_validation(json_data.get('token')):
                    return json.dumps({'status': -1, 'response': 'Valid token required!'})
            else:
                if request.content_type != 'application/json':
                    return json.dumps({'status': -1, 'response': 'Content-Type need to be application/json!'})

    def jobs(self):
        request_data = request.get_json() or {}

        status = 0
        if 'token' not in request_data:
            status = -1
            response = 'Invalid parameters!'
        else:
            response = self.controller.provide_data()

        return json.dumps({'status': status, 'response': response}, indent=4, sort_keys=True, default=str)

    def filter(self):
        request_data = request.get_json() or {}
        status, response = self.controller.filter(request_data["description"], request_data["type"],
                                                  request_data["tags"])
        return json.dumps({'status': status, 'response': response})

    def jobs_for_provider(self):
        request_data = request.get_json() or {}
        status, response = self.controller.jobs_for_provider(request_data)
        return json.dumps({'status' : status, 'response' : response})

    def applicants(self):
        request_data = request.get_json() or {}
        status, response = self.controller.view_applicants(request_data)

        return json.dumps({'status': status, 'response': response})
