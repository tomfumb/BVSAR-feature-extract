from os import path


def use_test_data_dir(monkeypatch_context) -> None:
    monkeypatch_context.setenv("src_data_dir", get_test_data_dir())


def get_test_data_dir() -> str:
    return path.join(path.dirname(__file__), "data")
