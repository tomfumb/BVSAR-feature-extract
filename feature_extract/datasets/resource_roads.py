from os import path

from osgeo import ogr
from settings import settings

from feature_extract.common import get_features_from_layer
from feature_extract.datasets.dataset_parameters import DatasetParameters
from feature_extract.datasets.dataset_provider import DatasetProvider


class ResourceRoads(DatasetProvider):
    def export_data(self, parameters: DatasetParameters) -> None:
        src_driver = ogr.GetDriverByName("OpenFileGDB")
        src_datasource = src_driver.Open(path.join(settings.src_data_dir, "FTEN_ROAD_SEGMENT_LINES_SVW.gdb"))
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
