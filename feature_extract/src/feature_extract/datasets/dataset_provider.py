from abc import ABC, abstractmethod
from os import environ, path
from re import escape, sub

from boto3 import session

from feature_extract.datasets.dataset_parameters import DatasetParameters


class DatasetProvider(ABC):
    def __init__(self):
        self.data_access_prefix = environ["data_access_prefix"]
        self.s3_data_source = self.data_access_prefix.startswith("/vsis3/")
        if self.s3_data_source:
            s3_config = {"service_name": "s3"}
            if "AWS_S3_ENDPOINT" in environ:
                use_https = environ.get("AWS_HTTPS", "YES") != "NO"
                s3_scheme = "https" if use_https else "http"
                s3_config["use_ssl"] = use_https
                s3_config["endpoint_url"] = "{}://{}".format(s3_scheme, environ["AWS_S3_ENDPOINT"])
            self.s3_client = session.Session().client(**s3_config)
            self.bucket_name = "/".join(self.data_access_prefix.split("/")[2:])

    @abstractmethod
    def export_data(self, parameters: DatasetParameters) -> None:
        pass

    @abstractmethod
    def get_dataset_name(self) -> str:
        pass

    @abstractmethod
    def get_layer_name(self) -> str:
        pass

    @abstractmethod
    def get_file_path(self) -> str:
        pass

    def cache_key(self) -> str:
        if self.s3_data_source:
            file_key = sub(rf"^{escape(self.data_access_prefix)}/", "", self.get_file_path())
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
            file_last_modified = response["LastModified"]
            return sub(r"[^\d]", "", str(file_last_modified))
        else:
            return str(path.getmtime(self.get_file_path()))
