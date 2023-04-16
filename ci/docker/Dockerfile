# Pull official base image
FROM python:3.10-slim

# Set work directory
WORKDIR /usr/src/app

#Create folder for database
RUN mkdir db

# Copy project files
COPY . .

#Install dependencies
RUN pip install -r requirements.txt

# Publish network port
EXPOSE 5000

# Execute script to start the application web server
ENTRYPOINT python new_bot.py
