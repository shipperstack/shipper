FROM alpine:3.19

# Install base dependencies
RUN apk update \
  && apk add --no-cache \
  python3=3.11.9-r0 \
  python3-dev=3.11.9-r0 \
  py3-pip=23.3.1-r0 \
  netcat-openbsd=1.226-r0 \
  gettext=0.22.3-r0 \
  git=2.43.4-r0 \
  postgresql15-client=15.7-r0 \
  libffi-dev=3.4.4-r3 \
  build-base=0.5-r3 \
  nodejs=20.12.1-r0 \
  npm=10.2.5-r0

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

# Copy Python dependency files
COPY requirements requirements
COPY requirements.txt requirements.txt

# Silence pip warnings
ENV PIP_NO_WARN_ABOUT_ROOT_USER=0

# Install Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Make Python dependencies available in PATH
ENV PATH="${HOME}/.local/bin:${PATH}"

# Copy server code
COPY . .

# chown all the files to the shipper user
RUN chown -R shipper:shipper $APP_HOME

# Change to the shipper user
USER shipper

# Frontend generation
# Warning: do not use --omit=dev, as webpack and bundler is required for building!
RUN npm install \
  && npm run build

ENTRYPOINT ["/bin/sh"]
