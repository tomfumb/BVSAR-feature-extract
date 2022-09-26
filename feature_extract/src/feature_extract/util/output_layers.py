from os import linesep

from feature_extract.common import get_dataset_providers


def execute(
    output_path: str,
) -> None:
    with open(output_path, "w") as f:
        f.writelines(linesep.join([provider.get_layer_name() for provider in get_dataset_providers()]))
        f.write(linesep)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("output_path")
    execute(parser.parse_args().output_path)
