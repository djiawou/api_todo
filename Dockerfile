FROM python:3.8-slim-buster
WORKDIR /app
COPY . /app/
RUN  python -m venv venv \
&& source venv/bin/active \
&& pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]
