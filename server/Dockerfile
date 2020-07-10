FROM python:3
RUN mkdir /server
WORKDIR /server
COPY ./requirements.txt /server/
COPY ./what /server/
RUN pip install -r requirements.txt
COPY ./* /server/