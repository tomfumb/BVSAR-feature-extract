#!/bin/bash

pushd $(dirname ${0})/..

layers_file=".bvsar-feature-extract-layers"
stack_common="docker-compose -f docker-compose.conversion.yml"
${stack_common} build
${stack_common} run --rm api python -m feature_extract.util.output_layers "/output/${layers_file}"
format=FlatGeobuf

IFS=$'\n'
set -f
for layer in $(cat < "/tmp/${layers_file}"); do

    echo
    read -p "Path to source file for layer ${layer} (include filename): " source_file_path
    echo ${source_file_path}
    read -p "Name of source layer for layer ${layer} [${layer}]: " source_layer
    layer_name=${source_layer:-$layer}
    echo ${layer_name}

    input_mount=$(dirname "${source_file_path}")
    input_file=$(basename "${source_file_path}")

    docker run \
        --rm \
        -v "${input_mount}":/input \
        -v "${PWD}/feature_extract/data":/output \
        osgeo/gdal:ubuntu-small-3.5.1 \
        ogr2ogr -f ${format} "/output/${layer}.fgb" "/input/${input_file}" "${layer_name}"

done
