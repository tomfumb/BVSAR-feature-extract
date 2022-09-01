from os import path

from pytest import MonkeyPatch

with MonkeyPatch.context() as mp:
    mp.setenv("src_data_dir", path.join(path.dirname(__file__), "data"))
    from feature_extract.datasets.dataset import Dataset
    from feature_extract.extract_parameters import ExtractParameters
    from feature_extract.retriever import count_features


def test_resource_roads_count():
    assert (
        count_features(
            ExtractParameters(
                lon_min=-127.41236,
                lon_max=-127.40352,
                lat_min=54.78662,
                lat_max=54.79261,
                dataset=Dataset.resource_roads,
            )
        )
        == 3
    )
