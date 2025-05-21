FROM python
ADD ./ .
RUN pip install python-dotenv uvicorn fastapi requests

CMD ["python", "./init.py"]