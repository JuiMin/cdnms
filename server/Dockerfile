FROM python:3.7
RUN mkdir /server
WORKDIR /server
COPY ./requirements.txt /server/
RUN pip install -r requirements.txt
COPY . /server/