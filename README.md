# BVSAR Feature Extract
Utility to extract individual feature data from BVSAR data store.

Currently extracts individual trails to GeoJSON from the source GeoPackage based on trail name. Ultimately should provide an interface to extract all spatial data (trails, shelters, resource roads) within a user-defined bounding box.

## Execute
`python feature-extract/local_features.py path-to-local-feature.gpkg path-to-output-dir`

## Development
Requires Python >= 3.8 and Poetry. Python GDAL package requires prior install of dependencies (not managed in this project).
- `scripts/init.sh` to install dependencies and configure pre-commit hooks
