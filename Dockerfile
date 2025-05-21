FROM python
RUN pip install uvicorn fastapi python-dotenv requests

COPY . .

EXPOSE 8000

ENV DEFAULT_PASSWORD="heslo"
ENV TABLE_NAME="tabulka"

CMD ["python", "docker_init.py"]