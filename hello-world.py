from flask import Flask, request
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import logging
import os

trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "hello-world-service"}))
)

# Otel Collector on localhost
# host.docker.internal is so we can forward otel data to "localhost" which is really the docker host (demo specific only)
otlp_exporter = OTLPSpanExporter(endpoint="http://host.docker.internal:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Initialize Flask app
app = Flask(__name__)

# Instrument Flask app
FlaskInstrumentor().instrument_app(app)

# Instrument logging
LoggingInstrumentor().instrument(set_logging_format=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def hello_world():
    response_message = os.getenv("RESPONSE_MESSAGE", "Hello, World!")
    logger.info(f"Handling request to / with message: {response_message}")

    return response_message


@app.route("/hello")
def hello():
    response = "there"
    # TODO Simulate DB call with random sleep to show metrics on how long a "db call" takes
    logger.info(response)
    return {"response": response}


@app.route("/metrics")
def metrics():
    return "Metrics endpoint"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
