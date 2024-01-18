import logging

from opentelemetry import trace, metrics
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def instrument_application(
    application,
    service_name: str,
    grpc_receiver_endpoint: str,
):
    resource = Resource.create(attributes={"service.name": service_name})

    trace.set_tracer_provider(TracerProvider(resource=resource))

    trace_provider: TracerProvider = trace.get_tracer_provider()

    otel_exporter = OTLPSpanExporter(endpoint=grpc_receiver_endpoint, insecure=True)

    span_processor = BatchSpanProcessor(span_exporter=otel_exporter)

    trace_provider.add_span_processor(span_processor)

    FastAPIInstrumentor.instrument_app(application)

    _instrument_logs(resource=resource, grpc_receiver_endpoint=grpc_receiver_endpoint)

    _instrument_metrics(
        resource=resource, grpc_receiver_endpoint=grpc_receiver_endpoint
    )

    RequestsInstrumentor().instrument()

    return application


def _instrument_logs(resource, grpc_receiver_endpoint: str) -> None:
    """

    Add open telemetry logs exporter to python logging.

    """

    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    logger_exporter = OTLPLogExporter(endpoint=grpc_receiver_endpoint, insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(logger_exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

    logger = logging.getLogger("pokeapi")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def _instrument_metrics(resource: Resource, grpc_receiver_endpoint: str) -> None:
    """

    Initialize open telemetry metrics exporter.

    """

    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=grpc_receiver_endpoint, insecure=True),
    )
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)
