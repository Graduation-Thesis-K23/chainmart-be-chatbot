FROM python:3.8-slim

RUN apt-get update && apt-get install

RUN apt-get install -y \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc \
  && apt-get clean

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements-socket.txt ./

USER root

RUN pip3 install --no-cache-dir -r requirements-socket.txt

COPY . /app

USER 1001

EXPOSE 5000

CMD [ "python3","/app/socket-io.py" ]