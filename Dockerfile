FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uvicorn fastapi python-dotenv requests

COPY . .

EXPOSE 8000

CMD ["python", "docker_init.py"]