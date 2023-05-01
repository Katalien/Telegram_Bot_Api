# Pull official base image
FROM python:3.10-slim

# Set work directory
WORKDIR /usr/src/app
# Copy project files
COPY . .

RUN ls -la
#Install dependencies
RUN pip install -r ./requirements.txt

# Install sqlite3
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3
#Create folder for database
RUN mkdir db
RUN mkdir attachments

# Publish network port
EXPOSE 5000

# Execute script to start the application web server
ENTRYPOINT python new_bot.py
