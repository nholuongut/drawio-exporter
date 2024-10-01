# syntax=docker/dockerfile:1
FROM python:3.9-slim-bullseye

LABEL com.example.version="1.18.0.1"
LABEL org.opencontainers.image.authors="https://github.com/Savamoti/docker-drawio-exporter"

ENV DRAWIO_VERSION "18.0.1"

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    xvfb \
    libgbm1 \
    libasound2

# Drawio app
WORKDIR /opt/drawio-desktop/
RUN wget -O drawio-desktop.deb -q https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-amd64-${DRAWIO_VERSION}.deb \
    && apt-get install -y ./drawio-desktop.deb \
    && rm -rf /opt/drawio-desktop/ \
    && rm -rf /var/lib/apt/lists/*

# Script
# drawio-desktop will not run from root user without argument "--no-sandbox".
# For some reason it can't export images if --no-sandbox argument not submitted last.
# And electron apps can't run without X-server. We need to set display.
# Xvfb is a virtual display server that implement the X11 display server.
# So you have to run it like this: xvfb-run -a /usr/bin/drawio ...some keys.. --no-sandbox.
WORKDIR /opt/scripts/
COPY drawio-exporter.py .
RUN chmod +x drawio-exporter.py \
    && export DISPLAY=:99 \
    && Xvfb :99 &

ENTRYPOINT ["/opt/scripts/drawio-exporter.py"]
CMD ["--help"]
