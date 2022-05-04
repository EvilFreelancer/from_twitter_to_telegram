FROM python:3.6

WORKDIR /app

RUN set -xe \
 && apt-get update \
 && apt-get install -fyqq curl bash \
 && apt-get clean

RUN set -xe \
 && pip install --upgrade pip \
 && pip install twython python-dotenv

COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]
