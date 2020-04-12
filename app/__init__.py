from flask import Flask, request, jsonify, abort, g
from config import Config
from app.models import db_setup, db, Log_entry
import time


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db_setup(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        status_code = response.status.split()[0]

        response_time = int((time.time() - g.start) * 1000)

        new_log_entry = Log_entry(
            request_method=request.method, path=request.path,
            status_code=status_code, response_time=response_time)

        new_log_entry.insert()

        return response

    # ERROR HANDLERS
    @app.errorhandler(400)
    def bad_request(error, message="Bad request"):
        return jsonify({
            "success": False,
            "error": 400,
            "message": message
        }), 400

    @app.errorhandler(404)
    def not_found(error, message="Not found"):
        return jsonify({
            "success": False,
            "error": 404,
            "message": message
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def not_found(error, message="Something went wrong."):
        return jsonify({
            "success": False,
            "error": 500,
            "message": message
        }), 500

    return app
