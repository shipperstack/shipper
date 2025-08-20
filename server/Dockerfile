FROM alpine:3.22

# Install base dependencies
RUN apk update \
  && apk add --no-cache \
  python3=3.12.11-r0 \
  python3-dev=3.12.11-r0 \
  py3-pip=24.3.1-r0 \
  netcat-openbsd=1.226.1.1-r0 \
  gettext=0.24.1-r0 \
  git=2.47.3-r0 \
  postgresql15-client=15.13-r0 \
  libffi-dev=3.4.7-r0 \
  build-base=0.5-r3 \
  nodejs=22.15.1-r0 \
  pnpm=9.15.9-r0

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

# Frontend generation (production)
RUN pnpm install -P \
  && pnpm run build

ENTRYPOINT ["/bin/sh"]
