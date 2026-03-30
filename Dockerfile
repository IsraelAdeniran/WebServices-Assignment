# Use Ubuntu as the base image
FROM ubuntu:22.04

# Author
LABEL authors="adefola"

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY app/requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the app folder
COPY app/ .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]