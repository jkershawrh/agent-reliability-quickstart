FROM registry.access.redhat.com/ubi9/python-312@sha256:8b1b36418501692d863a68f7f31ae47f1f169b83f7cdcc84831ac002304af693
ARG SOURCE_REVISION=unknown
LABEL org.opencontainers.image.source="https://github.com/jkershawrh/agent-reliability-quickstart" \
      org.opencontainers.image.revision="${SOURCE_REVISION}" \
      org.opencontainers.image.licenses="MIT"
WORKDIR /opt/app-root/src
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY config ./config
USER 1001
EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
