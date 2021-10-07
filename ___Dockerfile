#Python's Alpine Base Image
FROM python:3.6-alpine3.6

#Installing all python modules specified
COPY requirements.txt .
ADD requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Copy App Contents
ADD . /app
WORKDIR /app

#Start Flask Server
CMD [ "python","main.py"]
#Expose server port
EXPOSE 5000