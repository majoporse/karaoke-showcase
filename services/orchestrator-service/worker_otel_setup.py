"""OpenTelemetry initialization and setup for RQ worker"""

import logging
import os

logger = logging.getLogger(__name__)


def initialize_otel():
    """Initialize OpenTelemetry SDK for RQ worker

    Instruments RQ task execution with automatic tracing and metrics.
    """
    from opentelemetry import trace, metrics
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
        OTLPMetricExporter,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource
    from opentelemetry_instrumentation_rq import RQInstrumentor

    # Get OTEL collector endpoint from environment (required)
    otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not otel_endpoint:
        return

    # Create resource with service name and attributes
    resource = Resource.create(
        {
            "service.name": "orchestrator-worker",
            "service.version": "1.0.0",
        }
    )

    # ============ TRACES ============
    trace_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(trace_provider)
    trace_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=otel_endpoint))
    )
    logger.info(f"Traces configured: exporting to {otel_endpoint}")

    # ============ METRICS ============
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=otel_endpoint),
        export_interval_millis=5000,  # Export every 5 seconds
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    logger.info(f"Metrics configured: exporting to {otel_endpoint}")

    # ============ AUTO-INSTRUMENTATION ============
    # Auto-instrument RQ worker (traces + metrics for job execution)
    RQInstrumentor().instrument()
    logger.info("RQ instrumentation activated")

    logger.info("OpenTelemetry fully initialized: traces and metrics enabled")
