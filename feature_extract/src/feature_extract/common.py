from os import makedirs, path
from typing import Callable, List

from osgeo import ogr, osr

from feature_extract.datasets.dataset_provider import DatasetProvider
from feature_extract.extract_handler import ExtractHandler
from feature_extract.settings import settings

bbox_crs: str = "EPSG:4326"
result_dir: str = "src-data-export"
result_dir_path = path.join(settings.out_data_dir, result_dir)
makedirs(result_dir_path, exist_ok=True)
id_field_name: str = "id"
title_field_name: str = "title"
title_field_width: int = 100
result_layer_name: str = "result_layer"
handlers = {}


def register_handler(dataset: str, handler: DatasetProvider) -> None:
    handlers[dataset] = ExtractHandler(
        dataset_provider=handler,
        feature_type=ogr.wkbMultiLineString,
    )


def list_datasets() -> List[str]:
    return list(handlers.keys())


def get_features_from_layer(
    source_layer: ogr.Layer,
    destination_layer: ogr.Layer,
    title_provider: Callable[[ogr.Feature], str],
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
) -> None:
    memory_driver = ogr.GetDriverByName("Memory")
    clip_datasource = memory_driver.CreateDataSource("")
    clip_layer = clip_datasource.CreateLayer("clip_layer", geom_type=ogr.wkbPolygon)
    clip_geom = ogr.CreateGeometryFromWkt(
        f"POLYGON (({x_min} {y_min}, {x_max} {y_min}, {x_max} {y_max}, {x_min} {y_max}, {x_min} {y_min}))"
    )
    clip_srs = osr.SpatialReference()
    clip_srs.SetFromUserInput(bbox_crs)
    clip_geom.AssignSpatialReference(clip_srs)
    feature_defn = clip_layer.GetLayerDefn()
    feature = ogr.Feature(feature_defn)
    feature.SetGeometry(clip_geom)
    clip_layer.CreateFeature(feature)

    result_datasource = memory_driver.CreateDataSource("")
    result_layer = result_datasource.CreateLayer(
        "result_layer", geom_type=ogr.wkbMultiLineString
    )
    ogr.Layer.Clip(source_layer, clip_layer, result_layer)

    id_field = ogr.FieldDefn(id_field_name, ogr.OFTInteger64)
    title_field = ogr.FieldDefn(title_field_name, ogr.OFTString)
    title_field.SetWidth(title_field_width)
    destination_layer.CreateField(id_field)
    destination_layer.CreateField(title_field)
    while feature := result_layer.GetNextFeature():
        geometry_ref = feature.GetGeometryRef()
        new_geometry = geometry_ref.Clone()
        new_feature = ogr.Feature(destination_layer.GetLayerDefn())
        new_feature.SetGeometryDirectly(new_geometry)
        new_feature.SetField(id_field_name, feature.GetFID())
        new_feature.SetField(
            title_field_name, title_provider(feature)[0:title_field_width]
        )
        destination_layer.CreateFeature(new_feature)


def get_dataset_providers() -> List[DatasetProvider]:
    return [provider.dataset_provider for provider in handlers.values()]
