import os
import shared
from config import DevelopmentConfig
from flask import Flask, request
from shared import Authentication, User
from Project import get_project

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

@app.route('/')
def hello_world():
    return {
        'name': 'Ajit Jadhav'
    }

# -------------------------------- USER API ------------------------------------- #

# GET USER DETAILS
@app.route('/user', methods=['GET'])
def get_user():
    token = request.headers.get('Authorization', None)
    if token:
        token = token[len('Bearer '):]
        user = User(token)
        if user.verify():
            return {
                'status': 'Success',
                'data': user.get_user_data()
            }, 200
        else:
            return {
                'status': 'Failed',
                'error': 'Unauthorizedd'
            }, 401
    else:
        return {
            'status': 'Failed',
            'error': 'Unauthorized'
        }, 401


# GENERATE TOKEN
@app.route('/user/authenticate', methods=['POST'])
def authenticate_user():
    user_payload = request.get_json(force=True)
    if not user_payload:
        return {
            'status': 'Failed',
            'error': 'No payload'
        }, 401
    user = Authentication(user_payload)
    status, token, error = user.generate_token()
    if status:
        return {
            'status': 'Success',
            'data': {
                'token': {
                    'type': 'JWT',
                    'content': token
                }
            }
        }, 201
    else:
        return {
            'status': 'Failed',
            'error': error
        }, 401

# -------------------------------- PROJECT API ---------------------------------- #
@app.route('/project', methods=['GET'])
def get_project_details():
    token = request.headers.get('Authorization', None)
    if not token:
        return {
            'status': 'Failed',
            'error': 'Unauthorized'
        }, 401
    else:
        project_id = request.args.get('project_id', None)
        if not project_id:
            return {
                'status': 'Failed',
                'error': 'No Project ID'
            }, 401
        project_details, error = get_project(project_id)
        if project_details:
            return {
                'status': 'success',
                'data': project_details
            }, 200
        else:
            return {
                'status': 'Failed',
                'error': error
            }, 501

if __name__ == '__main__':
    app.run()