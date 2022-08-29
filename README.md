# BVSAR Feature Extract
Utility to extract individual feature data from BVSAR data stores.

Provides an interface to count and extract features within a given bounding box, clipped to that bounding box, from a specified dataset.

## Execution
### Environment
The following environment variables are mandatory:
- `src_data_dir`: identifies the parent directory containing all supported datasets. Datasets should not be in sub-directories.

The following environment variables are optional:
- `out_data_dir`: identifies the directory used to store generated datasets, defaults to a hidden directory relative to source code location. This could be a tmp directory, however this directory acts as a cache to avoid unnecessary processing for repeat requests and therefore should not be cleared unless storage constraints require it.

## Development
Requires Python >= 3.8 and Poetry. Python GDAL package requires prior install of dependencies (not managed in this project).
- `scripts/init.sh` to install dependencies and configure pre-commit hooks
