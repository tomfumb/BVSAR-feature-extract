from json import loads
from os import path

from osgeo import ogr
from pytest import MonkeyPatch
from tests.common import get_test_data_dir, use_test_data_dir

with MonkeyPatch.context() as mp:
    use_test_data_dir(mp)
    from feature_extract.datasets.providers.trails import DATASET_NAME as TRAILS
    from feature_extract.extract_parameters import ExtractParameters
    from feature_extract.retriever import count_features, get_features_file_path


extract_parameters = ExtractParameters(
    lon_min=101,
    lon_max=102,
    lat_min=-45,
    lat_max=-44,
    dataset=TRAILS,
)

test_feature_type = "test feature"
test_features = {
    "enclosed": "LINESTRING (101.1 -44.9, 101.1 -44.1, 101.9 -44.1)",
    "overlapping": "LINESTRING (101.1 -44.9, 101.1 -44.1, 101.9 -44.1, 102.1 -43.9, 102.1 -43.1, 105.5 -42)",
    "outside": "LINESTRING (102.1 -43.9, 102.1 -43.1, 105.5 -42)",
}

gpkg_name = "local-features.gpkg"
gpkg_path = path.join(get_test_data_dir(), gpkg_name)

trails_driver = ogr.GetDriverByName("GPKG")
trails_datasource = trails_driver.Open(gpkg_path, 1)
trails_layer = trails_datasource.GetLayerByName("trails")


def setup_function():
    for key, value in test_features.items():
        feature = ogr.Feature(trails_layer.GetLayerDefn())
        feature.SetField("name", key)
        feature.SetField("type", test_feature_type)
        shape = ogr.CreateGeometryFromWkt(value)
        feature.SetGeometry(shape)
        trails_layer.CreateFeature(feature)

    assert trails_layer.GetFeatureCount() == len(list(test_features.values())), "test setup problem creating features"


def teardown_function():
    fids = []
    while test_feature := trails_layer.GetNextFeature():
        fids.append(test_feature.GetFID())
    for fid in fids:
        trails_layer.DeleteFeature(fid)


def test_trails_count():
    assert count_features(extract_parameters) == 2


def test_trails_features():
    features_file_path = get_features_file_path(extract_parameters)
    result_driver = ogr.GetDriverByName("GeoJSON")
    result_datasource = result_driver.Open(features_file_path)
    result_layer = result_datasource.GetLayerByIndex(0)

    assert result_layer.GetFeatureCount() == 2, "incorrect number of features returned"

    def matchable_string(input: str) -> str:
        return input.replace(" ", "")

    while result_feature := result_layer.GetNextFeature():
        feature_geometry = result_feature.GetGeometryRef()
        feature_wkt = matchable_string(feature_geometry.ExportToWkt())
        feature_dict = loads(result_feature.ExportToJson())
        title = feature_dict["properties"]["title"]
        if title == f"enclosed ({test_feature_type})":
            assert feature_wkt == matchable_string(test_features["enclosed"])
        elif title == f"overlapping ({test_feature_type})":
            # original geometry will be clipped at export bbox edge
            assert feature_wkt == matchable_string("LINESTRING (101.1 -44.9, 101.1 -44.1, 101.9 -44.1, 102 -44)")
        else:
            raise Exception("Unexpected feature returned")
