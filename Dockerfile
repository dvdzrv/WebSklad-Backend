FROM python
RUN pip install uvicorn fastapi python-dotenv requests

COPY . .

EXPOSE 8000

CMD ["python", "docker_init.py"]