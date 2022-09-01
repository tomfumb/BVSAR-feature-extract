from abc import ABC, abstractmethod

from feature_extract.datasets.dataset_parameters import DatasetParameters


class DatasetProvider(ABC):
    @abstractmethod
    def export_data(self, parameters: DatasetParameters) -> None:
        pass
