from flask import make_response


def error_response(code: int, message: str):
    return (
        make_response({"status": "error", "code": code, "message": message}),
        code,
    )


def example_object_response(example_dict: dict, code: int = 200):
    return (
        make_response(
            {
                "key": example_dict["key"],
                "value": example_dict["value"],
            }
        ),
        code,
    )
