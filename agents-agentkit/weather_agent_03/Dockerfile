# Support custom base image
FROM agentkit-cn-beijing.cr.volces.com/base/py-simple:python3.12-bookworm-slim-latest

# === Only required when developing in a Zscaler environment ===
# 1. Copy and install Zscaler root CA certificate
COPY zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN apt-get update && apt-get install -y ca-certificates && \
    update-ca-certificates
# 2. Set environment variables to point to the merged system certificate library
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
# 3. Override Python certifi library certificate
RUN cp /etc/ssl/certs/ca-certificates.crt $(python -c "import certifi; print(certifi.where())")
# === End of Zscaler environment setup ===

ENV UV_SYSTEM_PYTHON=1 UV_COMPILE_BYTECODE=1 PYTHONUNBUFFERED=1 DOCKER_CONTAINER=1

COPY requirements.txt requirements.txt

RUN uv pip install -r requirements.txt

EXPOSE 8000

WORKDIR /app

# Copy entire project
COPY . .

CMD ["python", "-m", "simple_agent"]