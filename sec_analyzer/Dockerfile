FROM python:3
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY .env.example .env
COPY . /app
CMD ["python", "manage.py", "runserver", "makemigrations", "migrate", ""]

RUN python manage.py runserver makemigrations
RUN python manage.py migrate




