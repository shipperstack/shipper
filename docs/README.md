# README

This is the readme for the documentation of shipper, available at https://ericswpark.github.io/shipper.

## Build

To build and preview locally, run within the `docs/` directory:

```
pip3 install -r requirements.txt
mike serve
```

## Versioning

Deploy new versions with the following commands:

```
mike deploy --push --update-aliases 1.2.3 latest        # substitute 1.2.3 with version string
```

## Contributing

Make changes in a fork and submit a pull request.
