FROM python:3.11

WORKDIR /app

COPY requirements-docker.txt .

RUN pip install --upgrade pip

RUN pip install \
    --default-timeout=1000 \
    --retries 10 \
    -r requirements-docker.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]