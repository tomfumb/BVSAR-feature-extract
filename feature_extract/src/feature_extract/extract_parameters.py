from pydantic import BaseModel

from feature_extract.datasets.dataset import Dataset


class ExtractParameters(BaseModel):

    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    dataset: Dataset
