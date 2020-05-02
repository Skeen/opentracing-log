from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.sdk.trace import Span

import typing
import json

import structlog
structlog.configure(processors=[structlog.processors.JSONRenderer()])
trace_logger = structlog.get_logger()
output_logger = structlog.get_logger()


class LoggingSpanExporter(SpanExporter):
    """Implementation of :class:`SpanExporter` that logs spans as json."""

    def export(self, spans: typing.Sequence[Span]) -> SpanExportResult:
        for span in spans:
            trace_logger.info("OpenTelemetry Span", span=json.loads(span.to_json()))
        return SpanExportResult.SUCCESS

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(LoggingSpanExporter())
)
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span('outer'):
    with tracer.start_as_current_span('middle'):
        with tracer.start_as_current_span('inner'):
            output_logger.info("Hello world from OpenTelemetry Python!")
