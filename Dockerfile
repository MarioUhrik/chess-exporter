FROM python:3.9.10-slim-buster

WORKDIR /app

COPY manifests/conf/* conf/
COPY src/* .

RUN pip3 install \
  prometheus-client==0.13.1 \
  requests==2.21.0 \
  pyyaml==3.12

CMD python3 app.py
