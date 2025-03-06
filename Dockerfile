# Using official python runtime base image
FROM python:3.9-slim

# add curl for healthcheck
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the application directory
WORKDIR /app

# Install our requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy our code from the current folder to /app inside the container
COPY env/ /app/.env
COPY . .

# Make port 80 available for links and/or publish
EXPOSE 8000

# Define our command to be run when launching the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
