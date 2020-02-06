FROM python:alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

ENV PYTHONBUFFERED 1
WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000