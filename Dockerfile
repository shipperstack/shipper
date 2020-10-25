FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /shipper
WORKDIR /shipper
COPY requirements.txt /shipper/
RUN pip install -r requirements.txt
COPY . /shipper/
