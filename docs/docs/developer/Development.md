# Development

## Requirements

To develop for shipper, you need Docker installed.

## Initialization

Download the repository, and start up a development container by running the following command:

```
source activate
dcdup # docker-compose development up
```

To stop or restart, use `dcddown` and `dcdrestart`, respectively.

To see all commands, run `helpme`.

## Coding standards

shipper development uses the `black` formatter for formatting all Python code. Make sure to use `black` to format code before sending it in for PR.