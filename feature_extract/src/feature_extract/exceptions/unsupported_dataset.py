from feature_extract.datasets.dataset import Dataset


class UnsupportedDatasetException(Exception):
    def __init__(self, dataset: Dataset):
        self.dataset = dataset
