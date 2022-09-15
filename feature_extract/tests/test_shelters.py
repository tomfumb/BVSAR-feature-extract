from json import loads
from os import path

from osgeo import ogr
from pytest import MonkeyPatch
from tests.common import get_test_data_dir, use_test_data_dir

with MonkeyPatch.context() as mp:
    use_test_data_dir(mp)
    from feature_extract.datasets.providers.shelters import Shelters
    from feature_extract.extract_parameters import ExtractParameters
    from feature_extract.retriever import count_features, get_features_file_path


extract_parameters = ExtractParameters(
    lon_min=101,
    lon_max=102,
    lat_min=-45,
    lat_max=-44,
    dataset=Shelters().get_dataset_name(),
)

test_feature_type = "test feature"
test_features = {
    "enclosed": "POINT (101.1 -44.9)",
    "outside": "POINT (102.1 -43.9)",
}

gpkg_name = "local-features.gpkg"
gpkg_path = path.join(get_test_data_dir(), gpkg_name)

shelters_driver = ogr.GetDriverByName("GPKG")
shelters_datasource = shelters_driver.Open(gpkg_path, 1)
shelters_layer = shelters_datasource.GetLayerByName("shelters")


def setup_function():
    for key, value in test_features.items():
        feature = ogr.Feature(shelters_layer.GetLayerDefn())
        feature.SetField("name", key)
        shape = ogr.CreateGeometryFromWkt(value)
        feature.SetGeometry(shape)
        shelters_layer.CreateFeature(feature)

    assert shelters_layer.GetFeatureCount() == len(list(test_features.values())), "test setup problem creating features"


def teardown_function():
    fids = []
    while test_feature := shelters_layer.GetNextFeature():
        fids.append(test_feature.GetFID())
    for fid in fids:
        shelters_layer.DeleteFeature(fid)


def test_shelters_count():
    assert count_features(extract_parameters) == 1


def test_shelters_features():
    features_file_path = get_features_file_path(extract_parameters)
    result_driver = ogr.GetDriverByName("GeoJSON")
    result_datasource = result_driver.Open(features_file_path)
    result_layer = result_datasource.GetLayerByIndex(0)

    assert result_layer.GetFeatureCount() == 1, "incorrect number of features returned"

    while result_feature := result_layer.GetNextFeature():
        feature_geometry = result_feature.GetGeometryRef()
        feature_wkt = feature_geometry.ExportToWkt()
        feature_dict = loads(result_feature.ExportToJson())
        title = feature_dict["properties"]["title"]
        if title == "enclosed":
            assert feature_wkt == test_features["enclosed"]
        else:
            raise Exception("Unexpected feature returned")
