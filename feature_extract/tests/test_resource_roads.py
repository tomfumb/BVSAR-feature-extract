"""
Resource Roads data is delivered in File GeoDatabase format and OGR cannot edit this data.
Preferable to create test data during test setup and then destroy it, but because of
difficulties creating data use a reduced and stable real dataset instead.
"""

from json import loads

from osgeo import ogr
from pytest import MonkeyPatch
from tests.common import use_test_data_dir

with MonkeyPatch.context() as mp:
    use_test_data_dir(mp)
    from feature_extract.datasets.providers.resource_roads import (
        DATASET_NAME as RESOURCE_ROADS,
    )
    from feature_extract.extract_parameters import ExtractParameters
    from feature_extract.retriever import count_features, get_features_file_path


extract_parameters = ExtractParameters(
    lon_min=-127.41236,
    lon_max=-127.40352,
    lat_min=54.78662,
    lat_max=54.79261,
    dataset=RESOURCE_ROADS,
)


def test_resource_roads_count():
    assert count_features(extract_parameters) == 3


def test_resource_roads_features():
    features_file_path = get_features_file_path(extract_parameters)
    result_driver = ogr.GetDriverByName("GeoJSON")
    result_datasource = result_driver.Open(features_file_path)
    result_layer = result_datasource.GetLayerByIndex(0)
    expected_features = [
        {
            "title": "R16534 960",
            "vertices": 193,
        },
        {
            "title": "R16534 980",
            "vertices": 25,
        },
        {
            "title": "R16534 470",
            "vertices": 8,
        },
    ]
    assert len(expected_features) == result_layer.GetFeatureCount(), "incorrect number of features returned"
    found_feature_count = 0
    while result_feature := result_layer.GetNextFeature():
        feature_dict = loads(result_feature.ExportToJson())
        title = feature_dict["properties"]["title"]
        vertices = len(feature_dict["geometry"]["coordinates"])
        for expected_feature in expected_features:
            if title == expected_feature["title"] and vertices == expected_feature["vertices"]:
                found_feature_count += 1
    assert found_feature_count == len(expected_features), "returned features were not as expected"
