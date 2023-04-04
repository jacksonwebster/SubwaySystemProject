FROM python:3.8-slim-buster

WORKDIR /app

COPY subway_system.py .
COPY test_subway_system.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["bash", "-c", "python subway_flask_api.py & python test_subway_system.py"]