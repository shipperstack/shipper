FROM alpine:3.18

# Install base dependencies
RUN apk update \
  && apk upgrade \
  && apk add --no-cache \
  python3 \
  python3-dev \
  py3-pip \
  netcat-openbsd \
  gettext \
  git \
  postgresql-client \
  libffi-dev \
  build-base \
  nodejs \
  npm

# Upgrade pip
RUN pip3 install --upgrade pip

# Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create the shipper user
RUN adduser --disabled-password --home /home/shipper --shell /bin/sh shipper

# Environment and work directory setup
ENV HOME=/home/shipper
ENV APP_HOME=/home/shipper/web
WORKDIR $APP_HOME

# Create mountpoints
RUN mkdir -p $APP_HOME/media && \
  mkdir -p $APP_HOME/static

# Copy server code
COPY . .

# chown all the files to the shipper user
RUN chown -R shipper:shipper $APP_HOME

# Change to the shipper user
USER shipper

# Make Python dependencies available in PATH
ENV PATH="${HOME}/.local/bin:${PATH}"

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Frontend generation
RUN npm install \
  && npm run build

ENTRYPOINT ["/bin/sh"]
