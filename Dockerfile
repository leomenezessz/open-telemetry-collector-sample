FROM otel/opentelemetry-collector-contrib:0.92.0

ENV PORT 8888
ENV DATADOG_SITE $DATADOG_SITE
ENV DATADOG_API_KEY $DATADOG_API_KEY
ENV SENTRY_DNS $SENTRY_DNS

COPY otel-collector-config.yaml /etc/otelcol-contrib/config.yaml

EXPOSE 13133 4317 4318 8888
