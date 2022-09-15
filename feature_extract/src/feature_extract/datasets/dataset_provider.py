from abc import ABC, abstractmethod

from feature_extract.datasets.dataset_parameters import DatasetParameters


class DatasetProvider(ABC):
    @abstractmethod
    def export_data(self, parameters: DatasetParameters) -> None:
        pass

    @abstractmethod
    def cache_key(self) -> str:
        pass

    @abstractmethod
    def get_file_name(self) -> str:
        pass

    @abstractmethod
    def get_layer_name(self) -> str:
        pass
