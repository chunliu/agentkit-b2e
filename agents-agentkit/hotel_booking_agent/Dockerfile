FROM ubuntu:22.04 AS builder

RUN apt-get update && apt-get install -y curl
WORKDIR /build
RUN curl -L -o toolbox https://storage.googleapis.com/genai-toolbox/v0.24.0/linux/amd64/toolbox && \
    chmod +x toolbox

# Support custom base image
FROM agentkit-cn-beijing.cr.volces.com/base/py-simple:python3.12-bookworm-slim-latest

ENV UV_SYSTEM_PYTHON=1 UV_COMPILE_BYTECODE=1 PYTHONUNBUFFERED=1 DOCKER_CONTAINER=1

COPY requirements.txt requirements.txt

RUN uv pip install -r requirements.txt

EXPOSE 8000

WORKDIR /app

COPY --from=builder /build/toolbox .
# Copy entire project
COPY . .

CMD ["bash", "run.sh"]
