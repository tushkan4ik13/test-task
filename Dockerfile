FROM python:3.12.1-alpine as hello_api

RUN adduser -D app
USER app

WORKDIR /app

COPY source/requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

COPY source/ .

CMD [ "app_hello_api.py" ]
ENTRYPOINT [ "python3" ]
