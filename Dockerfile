FROM python:3.11-slim as base-image
ARG chatushka_version
WORKDIR /service
RUN pip install -v --pre chatushka==$chatushka_version
ENTRYPOINT ["chatushka"]
