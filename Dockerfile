FROM osgeo/gdal:ubuntu-small-3.5.1

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing \
  && apt-get install -y --no-install-recommends \
     build-essential \
     python3-dev \
     python3-pip \
  && apt-get clean
RUN pip install poetry
RUN echo "/usr/lib/python3.8/site-packages" >> /usr/local/lib/python3.8/dist-packages/site-packages.pth

WORKDIR /app
COPY feature_extract feature_extract
COPY feature_extract_api feature_extract_api
COPY pyproject.toml .

ARG POETRY_INSTALL_SUFFIX="--only=main"
WORKDIR /app/feature_extract
RUN poetry install ${POETRY_INSTALL_SUFFIX}
WORKDIR /app/feature_extract_api
RUN poetry install ${POETRY_INSTALL_SUFFIX}
WORKDIR /app
RUN poetry install ${POETRY_INSTALL_SUFFIX}

CMD [ "poetry", "run", "uvicorn", "feature_extract_api.app:app", "--host", "0.0.0.0", "--port", "80" ]
