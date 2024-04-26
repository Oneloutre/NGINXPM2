FROM python:3.12-alpine as builder

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt


COPY ./routes /app/routes
COPY ./static /app/static
COPY ./templates /app/templates
COPY ./app.py /app/
COPY ./ /app/
COPY ./requirements.txt /app/
COPY .env /app/

WORKDIR /app

# Exécuter l'application
CMD ["python", "app.py"]