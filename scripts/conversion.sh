#!/bin/bash

pushd $(dirname $0)/..

docker-compose build
layers=($(docker-compose run --rm api python -m feature_extract.util.print_layers))
format=FlatGeobuf

for layer in ${layers[@]}; do

    read -p "Path to source file for layer $layer: " source_file_path
    read -p "Name of source layer for layer $layer [$layer]: " source_layer

    input_mount="$(dirname $source_file_path)"
    input_file="$(basename $source_file_path)"

    docker run \
        --rm \
        -v $input_mount:/input \
        -v ${PWD}/feature_extract/data:/output \
        osgeo/gdal:ubuntu-small-3.5.1 \
        ogr2ogr -f ${format} /output/${layer}.fgb /input/${input_file} ${source_layer:-$layer}

done
