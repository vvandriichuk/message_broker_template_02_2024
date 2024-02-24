FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "/app/test_request_to_flask_api.py"]
