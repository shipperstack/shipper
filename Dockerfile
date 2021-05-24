FROM ubuntu:20.04

# Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create the shipper user
RUN useradd --create-home shipper

# Environment and work directory setup
ENV HOME=/home/shipper
ENV APP_HOME=/home/shipper/web
WORKDIR $APP_HOME

# Install base dependencies
RUN apt update && \
    apt install -y --no-install-recommends python3 python3-pip
    apt install -y --no-install-recommends python3 python3-pip netcat

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Create mountpoints
RUN mkdir -p $APP_HOME/media && \
    mkdir -p $APP_HOME/static

# Copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# Copy project
COPY . $APP_HOME

# chown all the files to the shipper user
RUN chown -R shipper:shipper $APP_HOME

# Change to the shipper user
USER shipper

# Run entrypoint.sh
ENTRYPOINT ["/home/shipper/web/entrypoint.sh"]
