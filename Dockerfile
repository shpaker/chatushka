FROM python:3.9-alpine as runtime-image
ARG CHATUSHKA_VERSION
RUN pip install "chatushka==$CHATUSHKA_VERSION"
ENTRYPOINT ["python3", "-m", "chatushka"]
