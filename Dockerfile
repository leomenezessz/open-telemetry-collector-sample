FROM otel/opentelemetry-collector-contrib:0.92.0

ARG DATADOG_SITE="datadoghq.com"
ARG DATADOG_API_KEY=""
ARG SENTRY_DNS=""

ENV DATADOG_SITE $DD_SITE
ENV DATADOG_API_KEY $DATADOG_API_KEY
ENV SENTRY_DNS $SENTRY_DNS

COPY otel-collector-config.yaml /etc/otelcol-contrib/config.yaml

ENTRYPOINT ["/otelcol"]

CMD ["--config=/etc/otelcol-contrib/config.yaml"]

EXPOSE 13133 4317 4318
