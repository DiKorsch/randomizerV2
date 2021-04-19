FROM python:3.9 AS randomizer

RUN apt-get update \
	&& apt-get upgrade -y \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000/tcp

