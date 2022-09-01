from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse

from feature_extract.datasets.dataset import Dataset
from feature_extract.extract_parameters import ExtractParameters
from feature_extract.retriever import count_features, get_features_file_path

app = FastAPI()


@app.get("/{dataset}/export/{x_min}/{y_min}/{x_max}/{y_max}")
async def export(dataset: Dataset, x_min: float, y_min: float, x_max: float, y_max: float) -> FileResponse:
    return FileResponse(
        get_features_file_path(
            ExtractParameters(
                lon_min=x_min,
                lon_max=x_max,
                lat_min=y_min,
                lat_max=y_max,
                dataset=dataset,
            )
        ),
        media_type="application/json",
    )


@app.get("/{dataset}/count/{x_min}/{y_min}/{x_max}/{y_max}")
async def count(dataset: Dataset, x_min: float, y_min: float, x_max: float, y_max: float) -> int:
    return count_features(
        ExtractParameters(
            lon_min=x_min,
            lon_max=x_max,
            lat_min=y_min,
            lat_max=y_max,
            dataset=dataset,
        )
    )


@app.get("/list")
async def export_types() -> List[str]:
    return [entry.value for entry in Dataset]
