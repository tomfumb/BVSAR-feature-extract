from feature_extract.common import get_dataset_providers

print(
    "{}".format(
        " ".join([provider.get_layer_name() for provider in get_dataset_providers()])
    )
)
