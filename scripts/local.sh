#!/bin/bash

pushd $(dirname $0)/..

pip install -e feature_extract[test]
pip install -e feature_extract_api[test]
pip install -r requirements.dev.txt

pre-commit install
