#!/bin/bash

function clean_up {
    rm -r dist/ build/ shipper_shippy.egg-info/
}

clean_up

# Build
python3 setup.py sdist bdist_wheel

# Upload
if [[ $1 == "-t" ]] ; then
    echo "Uploading to TestPyPI..."
    twine upload --repository testpypi dist/*
else
    echo "Uploading to PyPI..."
    twine upload dist/*
fi

clean_up