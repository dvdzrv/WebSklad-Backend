FROM python
RUN pip install uvicorn fastapi python-dotenv requests

COPY . .

COPY /home/.env_backend ./.env

EXPOSE 8000

CMD ["python", "docker_init.py;", "python", "init.py"]