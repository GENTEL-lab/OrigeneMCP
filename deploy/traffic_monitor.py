import json
import os
from datetime import datetime

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

NOW_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(os.path.dirname(NOW_DIR), "dist/logs")
os.makedirs(LOG_DIR, exist_ok=True)
TRAFFIC_LOG_FILE = os.path.join(LOG_DIR, "mcp_traffic.csv")


class SaveBodyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Save original request body
        body = await request.body()

        # Store request body in request.state
        request.state.raw_body = body

        # Try to parse different data formats
        content_type = request.headers.get("content-type", "").lower()

        if body:
            try:
                if "application/json" in content_type:
                    request.state.json_body = json.loads(body.decode("utf-8"))
                elif "application/x-www-form-urlencoded" in content_type:
                    from urllib.parse import parse_qs

                    body_str = body.decode("utf-8")
                    parsed = parse_qs(body_str)
                    # Simplify single value parameters
                    request.state.form_body = {
                        k: v[0] if len(v) == 1 else v for k, v in parsed.items()
                    }
                else:
                    request.state.text_body = body.decode("utf-8", errors="ignore")
            except Exception as e:
                request.state.body_parse_error = str(e)

        response = await call_next(request)
        return response


async def log_traffic(request_: Request, toolset: str, response):
    """Log tool call traffic"""
    # If file doesn't exist, create and write header
    if not os.path.exists(TRAFFIC_LOG_FILE):
        with open(TRAFFIC_LOG_FILE, "w", encoding="utf-8") as f:
            f.write("timestamp,toolset,method,url,client_ip,request_params,response\n")

    # Prepare log data
    timestamp = datetime.now().isoformat()
    method = request_.method
    url = str(request_.url)
    client_ip = request_.client.host

    # Get request body
    request_params = ""
    if request_.method in ["POST", "PUT"]:
        try:
            # Convert JSON parameters to string and replace characters that may affect CSV format
            params = request_.state.json_body.get("params", {})
            if (
                not params
                or "name" not in params.keys()
                or "arguments" not in params.keys()
            ):
                # No params, skip logging
                return
            request_params = (
                '"' + str(params).replace("\n", " ").replace('"', "'") + '"'
            )
        except Exception as e:
            request_params = str(e).replace(",", ";")

    # Get response content (limit length)
    response_str = str(response).replace(",", ";")[:100]

    # Write CSV line
    log_line = f"{timestamp},{toolset},{method},{url},{client_ip},{request_params},{response_str}\n"
    with open(TRAFFIC_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)
