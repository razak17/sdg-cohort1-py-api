from app.main import bp
from app.main.utils import estimates_schema
from flask import Flask, request, jsonify, abort, Response, g
from dicttoxml import dicttoxml
from marshmallow import ValidationError
from app.models import db, Log_entry
from app.estimator import estimator
import sys


@bp.route('/api/v1/on-covid-19', methods=['POST', 'GET'])
def function():
    request_payload = request.get_json()
    valid_payload = estimates_schema().load(request_payload)

    response_data = estimator(request_payload)
    return jsonify(response_data)


@bp.route('/api/v1/on-covid-19/', methods=['POST', 'GET'])
@bp.route('/api/v1/on-covid-19/<data_format>', methods=['POST', 'GET'])
def compute_estimates(data_format=None):
    if data_format not in ['xml', 'json', None]:
        abort(404)
    try:
        request_payload = request.get_json()
        valid_payload = estimates_schema().load(request_payload)

        response_data = estimator(request_payload)

        if data_format == 'xml':
            xml_data = dicttoxml(response_data)
            return Response(xml_data, mimetype='application/xml')

        elif data_format == 'json':
            return jsonify(response_data)
        return jsonify(response_data)

    except ValidationError:
        abort(400)

    except Exception:
        print(sys.exc_info())
        abort(500)


@bp.route('/api/v1/on-covid-19/logs')
def get_logs():
    try:
        api_logs = Log_entry.query.all()

        log_data = [entry.serialize() for entry in api_logs]

        formatted_log_data = ""

        for item in log_data:
            formatted_log_data += item + "\n"

        formatted_log_data = f"{formatted_log_data}"

        return Response(formatted_log_data, mimetype='text/plain')

    except Exception:
        print(sys.exc_info())
        abort(500)

    finally:
        db.session.close()
