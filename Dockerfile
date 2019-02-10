FROM python:3.6-alpine

RUN apk add gcc make musl-dev automake autoconf python3-dev libtool

WORKDIR /app
COPY alterego /app/alterego
COPY requeriments.txt /app/requeriments.txt
COPY entrypoint.sh /app/entrypoint.sh


RUN python -m pip install -r requeriments.txt

CMD ["python alterego/main.py"]