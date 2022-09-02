FROM osgeo/gdal:ubuntu-small-3.5.1

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing \
  && apt-get install -y --no-install-recommends \
     build-essential \
     python3-dev \
     python3-pip \
  && apt-get clean
RUN pip install poetry

WORKDIR /app
COPY feature_extract feature_extract
COPY feature_extract_api feature_extract_api
COPY pyproject.toml .

RUN poetry install --no-dev

CMD [ "feature_extract_api.app:app", "--host", "0.0.0.0", "--port", "80" ]