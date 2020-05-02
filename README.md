opentracing-log
---------------
Detached trace emition and exporting via logs.

# Installation
This project utilized unreleased features of opentracing:
```
git clone https://github.com/open-telemetry/opentelemetry-python.git
cd opentelemetry-python
pip install --upgrade -e ./opentelemetry-api
pip install --upgrade -e ./opentelemetry-sdk
pip install --upgrade -e ext/opentelemetry-ext-jaeger
```

# Usage
Run application and obtain a log file:
```
python tracing.py > log
```

Sometime later, start Jaeger using:
```
docker run -p 16686:16686 -p 6831:6831/udp jaegertracing/all-in-one
```

Process log file and upload spans to Jaeger:
```
python processor.py
```

See the result, namely the spans from the application inside Jaeger:
* http://localhost:16686/search
