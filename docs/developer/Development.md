# Development

## Coding standards

- Linting: `flake8` + `mccabe`
- Formatting: `black`

## Setting up a development environment

There are two ways of setting up a development environment.

### Set up with Docker (recommended)

Please see [the shipper-docker repository](https://github.com/shipperstack/shipper-docker/) for more information on how to set up a development environment with Docker.

### Set up manually

In this method you need to bring your own database (PostgreSQL). A web server (nginx) may also be installed alongside, but it is not necessary if you wish to just use Django's built-in web server.

A manual setup provides easy code reload, since changes will propagate immediately.
