from pydantic import BaseModel

from feature_extract.datasets.dataset_provider import DatasetProvider


class ExtractHandler(BaseModel):
    dataset_provider: DatasetProvider
    feature_type: int
