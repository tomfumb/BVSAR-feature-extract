from collections import defaultdict
from os import path, unlink
from re import sub

from osgeo.ogr import GetDriverByName, UseExceptions


def extract(
    gpkg_path: str,
    output_dir: str,
) -> None:
    UseExceptions()
    input_driver = GetDriverByName("GPKG")
    input_datasource = input_driver.Open(gpkg_path)
    trails_layer = input_datasource.GetLayerByName("trails")
    trails_by_name = defaultdict(list)
    while trail_feature := trails_layer.GetNextFeature():
        trail_name = trail_feature.GetFieldAsString("name").strip()
        trail_type = trail_feature.GetFieldAsString("type")
        trails_by_name[
            "{}{}".format(
                trail_name,
                f" ({trail_type})" if trail_type else "",
            )
        ].append(trail_feature)

    trails_output_driver = GetDriverByName("GeoJSON")
    trails_layer_defn = trails_layer.GetLayerDefn()
    for name, features in trails_by_name.items():
        safe_name = sub(r"[^a-zA-Z0-9\.\-\s\[\]\(\)\{\}]", "_", name)
        output_file = path.join(output_dir, f"{safe_name}.json")
        if path.exists(output_file):
            unlink(output_file)
        output_datasource = trails_output_driver.CreateDataSource(output_file)
        output_layer = output_datasource.CreateLayer(
            "layer",
            trails_layer.GetSpatialRef(),
            trails_layer_defn.GetGeomType(),
        )
        for feature in features:
            output_layer.CreateFeature(feature)

    # requires additional layer export for shelters
    # shelters_layer = input_datasource.GetLayerByName("shelters")


if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "gpkg_path",
        help="Absolute path to the local features GeoPackage file",
    )
    parser.add_argument(
        "output_dir",
        help="Absolute path to the feature output directory",
    )
    args = parser.parse_args()
    extract(
        args.gpkg_path,
        args.output_dir,
    )
