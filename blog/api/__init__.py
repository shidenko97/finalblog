import datetime
import time

from flask import Blueprint, g, request
from flask_restplus import Api
from rfc3339 import rfc3339

from blog.api.post import post_api
from blog.api.user import user_api
from blog.api.util.mongo_logger import log as mongo_logger


# Create API module and register instance
bp = Blueprint("api", __name__)
api = Api(
    bp,
    version="1.0",
    title="Final blog REST API",
    description="Simple REST API for my final blog with Flask-RESTPlus package"
)

# Register api namespaces
api.add_namespace(user_api)
api.add_namespace(post_api)


@bp.before_request
def start_timer():
    """Function that fire before any module view"""

    # Register API call time
    g.start = time.time()


@bp.after_request
def log_request(response):
    """Function that fire after any module view"""

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    host = request.host.split(":", 1)[0]
    args = request.json
    log_params = {
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "duration": duration,
        "time": timestamp,
        "ip": ip,
        "host": host,
        "params": args,
        "response": response.json if request.is_json else None
    }

    # Log request params
    mongo_logger.info(log_params)

    return response
