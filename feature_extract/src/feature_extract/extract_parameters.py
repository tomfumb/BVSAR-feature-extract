from pydantic import BaseModel


class ExtractParameters(BaseModel):

    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    dataset: str
