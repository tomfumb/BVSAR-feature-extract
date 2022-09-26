from pydantic import BaseModel


class ByteRangeParameters(BaseModel):

    range_start: int
    range_end: int
    dataset: str
