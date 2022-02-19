# Customization

shipper has a lot of environment variable settings to help you change how it looks and behaves, but to customize shipper and change how it processes build artifacts, you may have to make edits in the code and build Docker images for your own use.

## Why can't everything be done with environment variables?

Environment variables can't change the database schema written in `models.py`. To adapt shipper for your own project, more likely than not you would want to make changes to the schema, which requires editing the `models.py` file.

## Why can't build artifact matching/globing be done with environment variables?

shipper was originally designed to be used by BlissLabs for distributing BlissRoms artifacts. Therefore, it verifies the build artifact in several ways that is unique to the BlissRoms build artifacts. Unfortunately, the file name globing and verification is hard to code up as an environment variable, to the point where making changes and building a custom image would be an easier solution.

**Update**: I am working on a regex solution for globing/parsing file names. See the `filename-regex` branch for progress.

If you need to adapt shipper for your own organization or use, fork shipper, and make your changes. If any new commits are pushed to shipper, cherry-pick them into your fork. Any commits that can be shared with the main repository are welcome as a pull request.