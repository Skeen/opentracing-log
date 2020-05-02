from opentelemetry import trace
from opentelemetry.ext import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor

trace.set_tracer_provider(TracerProvider())

jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="my-helloworld-service", agent_host_name="localhost", agent_port=6831
)

trace.get_tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(jaeger_exporter)
)
tracer = trace.get_tracer(__name__)

print(trace.get_tracer_provider()._active_span_processor)
from opentelemetry.sdk.trace import Span
from opentelemetry.trace import SpanContext

import json
from datetime import datetime, timezone

def process_span(payload):
    # https://opentelemetry-python.readthedocs.io/en/latest/_modules/opentelemetry/trace.html#SpanContext
    payload_context = payload["context"]
    span_context = SpanContext(
        trace_id=int(payload_context["trace_id"], 16),
        span_id=int(payload_context["span_id"], 16),
        is_remote=False
    )
    parent_context = None
    if payload["parent_id"]:
        parent_context = SpanContext(
            trace_id=int(payload_context["trace_id"], 16),
            span_id=int(payload["parent_id"], 16),
            is_remote=False
        )
    # https://opentelemetry-python.readthedocs.io/en/stable/_modules/opentelemetry/sdk/trace.html#Span
    span = Span(
        name=payload["name"],
        context=span_context,
        # kind= # convert payload["kind"] to enum
        # parent= # convert payload["parent_id"] to parentspan
        parent=parent_context,
        span_processor=tracer.source._active_span_processor
    )
    def time_to_unixtime(dt):
        time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        datetime_object = datetime.strptime(dt, time_format)
        timestamp = datetime_object.replace(tzinfo=timezone.utc).timestamp()
        return int(timestamp * 1e9)

    span.start(start_time=time_to_unixtime(payload["start_time"]))
    # span.set_status(payload["status"])
    # TODO: attributes, events, links
    span.end(end_time=time_to_unixtime(payload["end_time"]))
    print(json.loads(span.to_json()))
    print(payload)
    print(json.loads(span.to_json()) == payload)


with open('log') as log_file:
    for line in log_file:
        payload = json.loads(line)
        if payload["event"] != "OpenTelemetry Span":
            continue
        process_span(payload["span"])
