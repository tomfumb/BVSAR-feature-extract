#!/bin/bash

pushd $(dirname $0)/..

docker-compose build
datasets=($(docker-compose run --rm api python -m feature_extract.util.print_datasets))
format=FlatGeobuf

for dataset in ${datasets[@]}; do

    file_name=$(echo $dataset | cut -d ":" -f 1)
    layer_name=$(echo $dataset | cut -d ":" -f 2)

    echo "converting ${file_name}:${layer_name} to ${format}"

    docker run \
        --rm \
        -v ${src_data_dir:-$PWD/feature_extract/data}:/input \
        -v ${PWD}/feature_extract/data:/output \
        osgeo/gdal:ubuntu-small-3.5.1 \
        ogr2ogr -f ${format} /output/${layer_name}.fgb /input/${file_name} ${layer_name}

done
