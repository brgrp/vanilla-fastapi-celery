FROM python:3.9-slim-buster

WORKDIR /app
ADD . /app

#--no-cache-dir
RUN pip install  -r requirements.txt
EXPOSE 80

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]