FROM python:3.11-slim

COPY . /app 
WORKDIR /app

RUN pip install django
RUN pip install django-cors-headers
RUN pip install djangorestframework

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# Adjust the CMD instruction to bind to 0.0.0.0:8000 for external access
CMD python3 spwise/manage.py runserver 0.0.0.0:8000
