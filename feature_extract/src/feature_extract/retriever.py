from hashlib import md5
from json import dumps
from os import path
from re import IGNORECASE, sub

from osgeo import ogr

from feature_extract.common import result_dir_path, result_layer_name
from feature_extract.datasets.dataset import Dataset
from feature_extract.datasets.dataset_parameters import DatasetParameters
from feature_extract.datasets.resource_roads import ResourceRoads
from feature_extract.extract_handler import ExtractHandler
from feature_extract.extract_parameters import ExtractParameters

handlers = {
    Dataset.resource_roads: ExtractHandler(
        dataset_provider=ResourceRoads(),
        feature_type=ogr.wkbMultiLineString,
    )
}


def _get_name_for_export(
    prefix: str, x_min: float, y_min: float, x_max: float, y_max: float
) -> str:
    return f"{prefix}-{md5(dumps([x_min, y_min, x_max, y_max]).encode('UTF-8')).hexdigest()}"


def get_features_file_path(
    parameters: ExtractParameters,
) -> str:
    result_driver = ogr.GetDriverByName("GeoJSON")
    result_filename_prefix = _get_name_for_export(
        sub(r"[^A-Z0-9\-_]+", "-", parameters.dataset.value, flags=IGNORECASE).lower(),
        parameters.lon_min,
        parameters.lat_min,
        parameters.lon_max,
        parameters.lat_max,
    )
    result_filename = f"{result_filename_prefix}.json"
    result_path = path.join(result_dir_path, result_filename)
    if not path.exists(result_path) or not parameters.permit_cache:
        result_datasource = result_driver.CreateDataSource(result_path)
        result_layer = result_datasource.CreateLayer(
            result_layer_name, geom_type=handlers[parameters.dataset].feature_type
        )
        handlers[parameters.dataset].export_data(
            DatasetParameters(
                lon_min=parameters.lon_min,
                lon_max=parameters.lon_max,
                lat_min=parameters.lat_min,
                lat_max=parameters.lat_max,
                result_layer=result_layer,
            )
        )

    return result_path


def count_features(
    parameters: ExtractParameters,
) -> int:
    result_driver = ogr.GetDriverByName("Memory")
    result_datasource = result_driver.CreateDataSource("")
    result_layer = result_datasource.CreateLayer(
        result_layer_name, geom_type=handlers[parameters.dataset].feature_type
    )
    handlers[parameters.dataset].dataset_provider.export_data(
        DatasetParameters(
            lon_min=parameters.lon_min,
            lon_max=parameters.lon_max,
            lat_min=parameters.lat_min,
            lat_max=parameters.lat_max,
            result_layer=result_layer,
        )
    )

    return result_layer.GetFeatureCount()
