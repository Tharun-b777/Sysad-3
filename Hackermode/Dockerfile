FROM python:3.7-alpine3.9
RUN apk update && apk add bash build-base python3-dev libffi-dev
WORKDIR /app
COPY ./python/ ./
COPY ./run.sh ./
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
RUN chmod +x ./run.sh
ENTRYPOINT ./run.sh
