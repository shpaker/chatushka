FROM python:3.9-alpine as runtime-image
ARG CHATUSHKA_VERION
RUN pip install chatushka==${CHATUSHKA_VERION}
ENTRYPOINT ["python3", "-m", "chatushka"]
