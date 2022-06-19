from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Bearer')


def verify_token(token):
    _token = ''
    return token == _token

