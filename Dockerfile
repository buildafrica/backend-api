FROM python:3.6-slim

LABEL maintainer="subomioluwalana71@gmail.com"

# Create Project Directory & Set it as working directory
RUN mkdir /mpa_app
WORKDIR /mpa_app

# Add application & Build Dependencies
ADD . /mpa_app
RUN pip install -r requirements/local.txt

# Environment Variables
ARG env
ARG name
ARG user
ARG passwd
ENV DCMPA_ENVIRONMENT=$env 
ENV POSTGRES_DB_NAME=$name
ENV POSTGRES_DB_USER=$user
ENV POSTGRES_USER_PASSWORD=$passwd

# Run make migrations, migrate & run tests
RUN python3 manage.py makemigrations && python3 manage.py migrate
RUN python3 manage.py test

EXPOSE 8080

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8080" ]