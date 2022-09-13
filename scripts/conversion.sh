#!/bin/sh

datasets=("FTEN_ROAD_SEGMENT_LINES_SVW.gdb:WHSE_FOREST_TENURE_FTEN_ROAD_SEGMENT_LINES_SVW" "local-features.gpkg:trails" "local-features.gpkg:shelters")

for dataset in ${datasets[@]}; do

    file_name=$(echo $dataset | cut -d ":" -f 1)
    layer_name=$(echo $dataset | cut -d ":" -f 2)

    # problems here if symlinks in data paths, preventing ogr2ogr from working

    docker run \
        --rm \
        -v ${src_data_dir}:/input \
        -v ${PWD}/feature_extract/data:/output \
        osgeo/gdal:ubuntu-small-3.5.1 \
        ogr2ogr -f FlatGeobuf /output/${layer_name}.fgb /input/${file_name} ${layer_name}

done
