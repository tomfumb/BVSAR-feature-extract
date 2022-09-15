from os import path

from osgeo import ogr

from feature_extract.common import get_features_from_layer, register_handler
from feature_extract.datasets.dataset_parameters import DatasetParameters
from feature_extract.datasets.dataset_provider import DatasetProvider
from feature_extract.settings import settings


class Trails(DatasetProvider):
    def __init__(self):
        self.dataset_name = "Trails"
        self.file_name = "local-features.gpkg"
        self.layer_name = "trails"
        self.fgb_file = f"{self.layer_name}.fgb"
        self.gpkg_path = path.join(settings.src_data_dir, self.file_name)

    def export_data(self, parameters: DatasetParameters) -> None:
        src_driver = ogr.GetDriverByName("FlatGeobuf")
        src_url = f"/vsis3/{settings.s3_bucket_name}/{self.fgb_file}"
        src_datasource = src_driver.Open(src_url)
        src_layer = src_datasource.GetLayerByIndex(0)

        def title_provider(feature: ogr.Feature) -> str:
            name = feature.GetFieldAsString("name")
            type = feature.GetFieldAsString("type")
            suffix = f" ({type})" if type else ""
            return f"{name}{suffix}"

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

    def get_dataset_name(self) -> str:
        return self.dataset_name

    def get_file_name(self) -> str:
        return self.file_name

    def get_layer_name(self) -> str:
        return self.layer_name


register_handler(Trails())
