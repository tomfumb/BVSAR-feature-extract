from enum import Enum


class Dataset(str, Enum):
    resource_roads = "Resource Roads"
    trails = "Trails"
    shelters = "Shelters"
