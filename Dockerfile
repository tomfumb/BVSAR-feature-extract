FROM osgeo/gdal:ubuntu-small-3.5.1

# ARG DEBIAN_FRONTEND=noninteractive
# RUN apt-get update --fix-missing \
#   && apt-get install -y --no-install-recommends \
#      python3-pip \
#   && apt-get clean
# RUN pip install poetry

# WORKDIR /setup
# COPY pyproject.toml .
# RUN poetry install --no-dev

COPY feature-extract /extract
