FROM python:3.6

RUN apt-get update && \
    apt-get install -y && \
    pip install uwsgi

ENV APP_PATH /opt/app/
RUN mkdir -p $APP_PATH

WORKDIR $APP_PATH 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV DJANGO_ENV=prod
ENV DOCKER_CONTAINER=1

EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]

