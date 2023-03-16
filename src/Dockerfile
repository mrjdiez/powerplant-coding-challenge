FROM python:3.9.16-alpine

WORKDIR /etc/bin
COPY . .

RUN pip3 install -r requirements.txt
EXPOSE 8888
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=8888
ENV FLASK_RUN_HOST=0.0.0.0

HEALTHCHECK --interval=5m --timeout=5s CMD curl https://localhost:8888/

ENTRYPOINT flask run