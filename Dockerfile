FROM python:3.5

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY server.py requirements.txt /usr/src/app/
COPY ${DELI_SSL_CERTS}/server.key ${DELI_SSL_CERTS}/server.crt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "server.py", "0.0.0.0", "1234"]