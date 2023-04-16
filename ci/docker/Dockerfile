# Pull official base image
FROM python:3.10-slim

# Set work directory
WORKDIR /usr/src/app

#COPY pip.conf /etc/pip.conf
#
## Set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#
## Install dependencies
#COPY pip.conf /etc/pip.conf
#COPY Pipfile.lock Pipfile ./
#
#RUN pip install -U pip pipenv && pipenv install --system --deploy --ignore-pipfile --dev

# Copy project files
COPY . .

## Make entrypoint.sh executable
#RUN chmod +x ./entrypoint.sh

# Publish network port
EXPOSE 5000

# Execute script to start the application web server
#ENTRYPOINT ["./entrypoint.sh"]
ENTRYPOINT python new_bot.py
