from abc import ABC, abstractmethod
from uuid import uuid4

from feature_extract.datasets.dataset_parameters import DatasetParameters


class DatasetProvider(ABC):
    @abstractmethod
    def export_data(self, parameters: DatasetParameters) -> None:
        pass

    @abstractmethod
    def get_dataset_name(self) -> str:
        pass

    @abstractmethod
    def get_file_name(self) -> str:
        pass

    @abstractmethod
    def get_layer_name(self) -> str:
        pass

    @abstractmethod
    def get_file_path(self) -> str:
        pass

    def cache_key(self) -> str:
        # TODO: use last modified property of self.get_file_path()
        return str(uuid4())
