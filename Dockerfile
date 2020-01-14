FROM python:3.6.10-slim

COPY . /app
WORKDIR /app
RUN apt update && \
	apt install ffmpeg -y && \
	pip install pipenv && \
	pipenv install

ENTRYPOINT ["pipenv", "run", "python", "convert.py"]
