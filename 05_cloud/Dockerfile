FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PORT=8080

COPY 05_cloud/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "python -m uvicorn 04_app.server:app --host 0.0.0.0 --port ${PORT}"]
