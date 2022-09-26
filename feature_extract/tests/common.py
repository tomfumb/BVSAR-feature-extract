from os import path


def use_test_data_dir(monkeypatch_context) -> None:
    monkeypatch_context.setenv("data_access_prefix", get_test_data_dir())


def get_test_data_dir() -> str:
    return path.join(path.dirname(__file__), "data")
