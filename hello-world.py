from flask import Flask, request
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import logging

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "hello-world-service"})
    )
)

otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
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

@app.route('/')
def hello_world():
    logger.info("Handling request to /")
    return 'Hello, World!'

@app.route('/hello')
def hello():
    logger.info("there")
    return {"there":"maybe"}


@app.route('/metrics')
def metrics():
    return 'Metrics endpoint'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
