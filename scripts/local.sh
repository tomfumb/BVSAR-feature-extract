#!/bin/bash

pushd $(dirname $0)/..

pushd feature_extract
poetry install
popd
pushd feature_extract_api
poetry install
popd
poetry install

pre-commit install
