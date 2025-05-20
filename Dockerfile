#using base image
FROM python:3.11.3-slim-buster

#set working directory in container
WORKDIR /app

#copy the current directory contents into container at /app
COPY . /app

# updating all packages
RUN apt update -y && apt install awscli -y

#install dependices
RUN pip install -r requirements.txt

#Run the app
CMD ["python3","app.py"]