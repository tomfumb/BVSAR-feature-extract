from os import path

from osgeo import ogr

from feature_extract.common import get_features_from_layer, register_handler
from feature_extract.datasets.dataset import Dataset
from feature_extract.datasets.dataset_parameters import DatasetParameters
from feature_extract.datasets.dataset_provider import DatasetProvider
from feature_extract.settings import settings


class Shelters(DatasetProvider):
    def __init__(self):
        self.gpkg_path = path.join(settings.src_data_dir, "local-features.gpkg")

    def export_data(self, parameters: DatasetParameters) -> None:
        src_driver = ogr.GetDriverByName("GPKG")
        src_datasource = src_driver.Open(self.gpkg_path)
        src_layer = src_datasource.GetLayerByName("shelters")

        def title_provider(feature: ogr.Feature) -> str:
            return feature.GetFieldAsString("name")

        get_features_from_layer(
            src_layer,
            parameters.result_layer,
            title_provider,
            parameters.lon_min,
            parameters.lat_min,
            parameters.lon_max,
            parameters.lat_max,
        )

    def cache_key(self) -> str:
        return str(path.getmtime(self.gpkg_path))


register_handler(Dataset.shelters, Shelters())
