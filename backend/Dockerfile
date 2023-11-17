FROM python:3.12.0-slim-bullseye

WORKDIR /backend

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /backend/project

RUN python manage.py migrate

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]