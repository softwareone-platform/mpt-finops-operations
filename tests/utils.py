from typing import Any

from pydantic.alias_generators import to_snake

from app.models import UUIDModel


def assert_json_contains_model(json: dict[str, Any], expected_model: UUIDModel) -> None:
    assert all("id" in item for item in json["items"])

    items_by_id = {item["id"]: item for item in json["items"]}

    assert str(expected_model.id) in list(items_by_id.keys())

    expected_dict = expected_model.model_dump(mode="json")
    actual_dict = items_by_id[str(expected_model.id)]

    for key, actual_value in actual_dict.items():
        if to_snake(key) not in expected_dict:
            raise AssertionError(f"{expected_model} has no attribute {to_snake(key)}")

        expected_value = expected_dict[to_snake(key)]
        assert expected_value == actual_value
