FROM python:3.10.1

RUN apt update -y
RUN apt upgrade -y

# set this to prevent buffering for logging
ENV PYTHONUNBUFFERED 1

WORKDIR /ws-dj

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY . .