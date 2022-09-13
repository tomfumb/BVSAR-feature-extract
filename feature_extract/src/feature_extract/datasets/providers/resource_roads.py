from os import path
from typing import Final

from osgeo import ogr

from feature_extract.common import get_features_from_layer, register_handler
from feature_extract.datasets.dataset_parameters import DatasetParameters
from feature_extract.datasets.dataset_provider import DatasetProvider
from feature_extract.settings import settings

DATASET_NAME: Final = "Resource Roads"


class ResourceRoads(DatasetProvider):
    def __init__(self):
        self.fgdb_path = path.join(settings.src_data_dir, "FTEN_ROAD_SEGMENT_LINES_SVW.gdb")

    def export_data(self, parameters: DatasetParameters) -> None:
        src_driver = ogr.GetDriverByName("OpenFileGDB")
        src_datasource = src_driver.Open(self.fgdb_path)
        src_layer = src_datasource.GetLayerByIndex(0)

        def title_provider(feature: ogr.Feature) -> str:
            name = feature.GetFieldAsString("MAP_LABEL")
            status = " (retired)" if feature.GetFieldAsString("LIFE_CYCLE_STATUS_CODE") == "RETIRED" else ""
            return f"{name}{status}"

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
        return str(path.getmtime(path.join(self.fgdb_path, "timestamps")))


register_handler(DATASET_NAME, ResourceRoads())
