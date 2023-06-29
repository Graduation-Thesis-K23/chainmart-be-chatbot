# Extend the official Rasa SDK image
FROM rasa/rasa:3.6.0-full

WORKDIR /app


USER root


COPY . /app

USER 1001

CMD ["run"]
