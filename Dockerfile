# #using base image
# FROM python:3.11.3-slim-buster

# #set working directory in container
# WORKDIR /app

# #copy the current directory contents into container at /app
# COPY . /app

# # updating all packages
# RUN apt update -y && apt install awscli -y

# #install dependices
# RUN pip install  -r requirements.txt

# #Run the app
# CMD ["python3","app.py"]

# Use base image
FROM python:3.11-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    build-essential \
    awscli \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (to use cache better)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy all project files (after venv is excluded via .dockerignore)
COPY . .

# Run the app
CMD ["python3", "app.py"]
