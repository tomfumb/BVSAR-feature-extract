class UnsupportedDatasetException(Exception):
    def __init__(self, dataset: str):
        self.dataset = dataset
