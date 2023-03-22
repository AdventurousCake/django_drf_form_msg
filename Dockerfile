# pull official base image
FROM python:3.11-alpine

# create the app user
RUN addgroup -S app_user && adduser -S app_user -G app_user
#RUN adduser -D app_user

# set work directory
ENV APP_HOME=/usr/src/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install psycopg2 dependencies
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# chown all the files to the app user
RUN chown -R app_user:app_user $APP_HOME
USER app_user

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
