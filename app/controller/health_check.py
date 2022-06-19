from flask import Blueprint

check = Blueprint('check', __name__, url_prefix='/api')


@check.route('/alive', methods=['GET'])
def health_check():
    return 'OK'
