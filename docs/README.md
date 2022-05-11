# README

This is the readme for the documentation of shipper, available at https://ericswpark.github.io/shipper.

## Build

To build and preview locally, run within the `docs/` directory:

```
pip3 install -r requirements.txt
mike serve
```

## Versioning

The `master` version is always deployed by GitHub Actions whenever a new commit lands in the `master` branch.

To "preserve" the current state of the documentation for version X, run the following command, replacing X with the version string:

```
mike deploy --push X    # Replace X with version string, like 1.15
```

Do not archive patch versions (like 1.15.2).

## Contributing

Make changes in a fork and submit a pull request.
