from os import path


def use_test_data_dir(monkeypatch_context):
    monkeypatch_context.setenv(
        "src_data_dir", path.join(path.dirname(__file__), "data")
    )
