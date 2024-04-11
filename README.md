# OpenTelemetry Python `structlog` Handler Example
This is a demo for the custom structlog handler implemented for OpenTelemetry. Overall, this example runs a basic Flask application to demonstrate an example application that uses OpenTelemetry logging with Python's logging library structlog. This example is scalable to other software systems that require the use of the structlog library for logging.

Note: This example is adapted from OpenTelemetry's [Getting Started Tutorial for Python](https://opentelemetry.io/docs/languages/python/getting-started/) guide.

## Prerequisites
Python 3

## Installation
Prior to building the example application, set up the directory and virtual environment:
```
mkdir otel-getting-started
cd otel-getting-started
python3 -m venv venv
source ./venv/bin/activate
```

After activating the virtual environment `venv`, install flask.
```
pip install flask
```

### Create and Launch HTTP Server
Now that the environment is set up, create an `app.py ` flask application. This is a basic example that uses the structlog Python logging library for OpenTelemetry logging instead of the standard Python logging library. Notice the importance of the following imports for using the structlog handler: `import structlog` and `from handlers.opentelemetry_structlog.src.exporter import StructlogHandler`.

```
from random import randint
from flask import Flask, request
import structlog
from handlers.opentelemetry_structlog.src.exporter import StructlogHandler

app = Flask(__name__)


# Create a Structlog logger
structlog.configure(logger_factory=structlog.PrintLoggerFactory())
logger = structlog.get_logger()

# Create an instance of the StructlogHandler
handler = StructlogHandler(service_name="flask-structlog-demo", server_hostname="instance-1", exporter=None)

# Set the logger to use the StructlogHandler
logger.bind(handler=handler)



@app.route("/rolldice")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    result = str(roll())
    if player:
        logger.warning("%s is rolling the dice: %s", player, result)
    else:
        logger.warning("Anonymous player is rolling the dice: %s", result)
    return result


def roll():
    return randint(1, 6)
```

Run the application on port 8080 with the following flask command and open [http://localhost:8080/rolldice](http://localhost:8080/rolldice) in your web browser to ensure it is working.

```
flask run -p 8080
```

## Instrumentation

Automatic instrumentation will generate telemetry data on your behalf. There are several options you can take, covered in more detail in [Automatic Instrumentation](https://opentelemetry.io/docs/languages/python/automatic/). Here we’ll use the `opentelemetry-instrument` agent.

Install the `opentelemetry-distro` package, which contains the OpenTelemetry API, SDK and also the tools `opentelemetry-bootstrap` and `opentelemetry-instrument` you will use below.

```
pip install opentelemetry-distro
```

Run the `opentelemetry-bootstrap` command:

```
opentelemetry-bootstrap -a install
```

This will install Flask instrumentation.

## Run the Instrumented App

You can now run your instrumented app with `opentelemetry-instrument` and have it print to the console for now:

```
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name dice-server \
    flask run -p 8080
```

Open [http://localhost:8080/rolldice](http://localhost:8080/rolldice) in your web browser and reload the page a few times. After a while you should see the spans printed in the console, such as the following example output.

Notice the first line in the example output is the relevant to the structlog handler.

Example Output:

```
2024-04-11 16:49:31 [warning  ] Anonymous player is rolling the dice: 6
{
    "name": "/rolldice",
    "context": {
        "trace_id": "0xc4fe8c1c15980f456097bd99c2f0229b",
        "span_id": "0x65eccb1343750cb6",
        "trace_state": "[]"
    },
    "kind": "SpanKind.SERVER",
    "parent_id": null,
    "start_time": "2024-04-11T20:49:31.370819Z",
    "end_time": "2024-04-11T20:49:31.376794Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "http.method": "GET",
        "http.server_name": "127.0.0.1",
        "http.scheme": "http",
        "net.host.port": 8080,
        "http.host": "localhost:8080",
        "http.target": "/rolldice",
        "net.peer.ip": "127.0.0.1",
        "http.user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "net.peer.port": 51620,
        "http.flavor": "1.1",
        "http.route": "/rolldice",
        "http.status_code": 200
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.24.0",
            "service.name": "dice-server",
            "telemetry.auto.version": "0.45b0"
        },
        "schema_url": ""
    }
}
{
    "body": "127.0.0.1 - - [11/Apr/2024 16:49:31] \"GET /rolldice HTTP/1.1\" 200 -",
    "severity_number": "<SeverityNumber.INFO: 9>",
    "severity_text": "INFO",
    "attributes": {
        "otelSpanID": "0",
        "otelTraceID": "0",
        "otelTraceSampled": false,
        "otelServiceName": "dice-server",
        "code.filepath": "/Users/carolinegilbert/Desktop/2023-24/SPRING_24/ECE595/testing/structlog-demo/my_demo_venv/lib/python3.11/site-packages/werkzeug/_internal.py",
        "code.function": "_log",
        "code.lineno": 96
    },
    "dropped_attributes": 0,
    "timestamp": "2024-04-11T20:49:31.377386Z",
    "observed_timestamp": "2024-04-11T20:49:31.377446Z",
    "trace_id": "0x00000000000000000000000000000000",
    "span_id": "0x0000000000000000",
    "trace_flags": 0,
    "resource": "{'telemetry.sdk.language': 'python', 'telemetry.sdk.name': 'opentelemetry', 'telemetry.sdk.version': '1.24.0', 'service.name': 'dice-server', 'telemetry.auto.version': '0.45b0'}"
}
{
    "resource_metrics": [
        {
            "resource": {
                "attributes": {
                    "telemetry.sdk.language": "python",
                    "telemetry.sdk.name": "opentelemetry",
                    "telemetry.sdk.version": "1.24.0",
                    "service.name": "dice-server",
                    "telemetry.auto.version": "0.45b0"
                },
                "schema_url": ""
            },
            "scope_metrics": [
                {
                    "scope": {
                        "name": "opentelemetry.instrumentation.flask",
                        "version": "0.45b0",
                        "schema_url": "https://opentelemetry.io/schemas/1.11.0"
                    },
                    "metrics": [
                        {
                            "name": "http.server.active_requests",
                            "description": "measures the number of concurrent HTTP requests that are currently in-flight",
                            "unit": "requests",
                            "data": {
                                "data_points": [
                                    {
                                        "attributes": {
                                            "http.method": "GET",
                                            "http.host": "localhost:8080",
                                            "http.scheme": "http",
                                            "http.flavor": "1.1",
                                            "http.server_name": "127.0.0.1"
                                        },
                                        "start_time_unix_nano": 1712868571370992000,
                                        "time_unix_nano": 1712868620973649000,
                                        "value": 0
                                    }
                                ],
                                "aggregation_temporality": 2,
                                "is_monotonic": false
                            }
                        },
                        {
                            "name": "http.server.duration",
                            "description": "Duration of HTTP client requests.",
                            "unit": "ms",
                            "data": {
                                "data_points": [
                                    {
                                        "attributes": {
                                            "http.method": "GET",
                                            "http.host": "localhost:8080",
                                            "http.scheme": "http",
                                            "http.flavor": "1.1",
                                            "http.server_name": "127.0.0.1",
                                            "net.host.port": 8080,
                                            "http.status_code": 200
                                        },
                                        "start_time_unix_nano": 1712868571376956000,
                                        "time_unix_nano": 1712868620973649000,
                                        "count": 1,
                                        "sum": 6,
                                        "bucket_counts": [
                                            0,
                                            0,
                                            1,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0,
                                            0
                                        ],
                                        "explicit_bounds": [
                                            0.0,
                                            5.0,
                                            10.0,
                                            25.0,
                                            50.0,
                                            75.0,
                                            100.0,
                                            250.0,
                                            500.0,
                                            750.0,
                                            1000.0,
                                            2500.0,
                                            5000.0,
                                            7500.0,
                                            10000.0
                                        ],
                                        "min": 6,
                                        "max": 6
                                    }
                                ],
                                "aggregation_temporality": 2
                            }
                        }
                    ],
                    "schema_url": "https://opentelemetry.io/schemas/1.11.0"
                }
            ],
            "schema_url": ""
        }
    ]
}
```

# structlog-demo
