FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN  python -m venv venv && pip install -r requirements.txt

COPY . /app/

CMD ["flask", "run"]
