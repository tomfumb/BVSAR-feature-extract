from json import dumps
from os import path
from tempfile import gettempdir
from unittest import mock
from uuid import uuid4

from fastapi.testclient import TestClient

from feature_extract.common import list_datasets
from feature_extract.datasets.providers.resource_roads import (
    DATASET_NAME as RESOURCE_ROADS,
)
from feature_extract.extract_parameters import ExtractParameters
from feature_extract_api.app import app

client = TestClient(app)


def test_list():
    response = client.get("/list")
    assert response.status_code == 200
    response_datasets = response.json()
    assert len(response_datasets) == len(list_datasets())


@mock.patch("feature_extract_api.app.count_features")
def test_count_features(
    count_features_mock: mock.MagicMock,
):
    count = 3
    count_features_mock.return_value = count
    dataset, x_min, x_max, y_min, y_max = RESOURCE_ROADS, -180, 180, -90, 90
    response = client.get(f"/{dataset}/count/{x_min}/{y_min}/{x_max}/{y_max}")
    assert response.status_code == 200
    assert response.json() == count
    count_features_mock.assert_called_once_with(
        ExtractParameters(
            lon_min=x_min,
            lon_max=x_max,
            lat_min=y_min,
            lat_max=y_max,
            dataset=dataset,
        )
    )


@mock.patch("feature_extract_api.app.get_features_file_path")
def test_export_features(
    get_features_file_path_mock: mock.MagicMock,
):
    export_file_path = path.join(gettempdir(), f"{uuid4()}.json")
    export_content = {"value": str(uuid4())}
    with open(path.join(export_file_path), "w") as f:
        f.write(dumps(export_content))
    get_features_file_path_mock.return_value = export_file_path
    dataset, x_min, x_max, y_min, y_max = RESOURCE_ROADS, -180, 180, -90, 90
    response = client.get(f"/{dataset}/export/{x_min}/{y_min}/{x_max}/{y_max}")
    assert response.status_code == 200
    assert response.json() == export_content
    get_features_file_path_mock.assert_called_once_with(
        ExtractParameters(
            lon_min=x_min,
            lon_max=x_max,
            lat_min=y_min,
            lat_max=y_max,
            dataset=dataset,
        )
    )
