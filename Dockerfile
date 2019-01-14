FROM alpine:3.8

WORKDIR /app
COPY . /app

RUN apk add python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
rm -r /root/.cache

RUN apk add gcc make musl-dev automake autoconf python3-dev libtool

RUN pip3 install -r requeriments.txt

ENTRYPOINT ["./entrypoint.sh"]