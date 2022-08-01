from flask import make_response


def error_response(code: int, message: str):
    return (
        make_response({"status": "error", "code": code, "message": message}),
        code,
    )


def event_object_response(event_dict: dict, code: int = 200):
    return (
        make_response(
            {
                "id": event_dict["id"],
                "code": event_dict["code"],
                "entity_identifier": event_dict["entity_identifier"],
                "timestamp": event_dict["timestamp"],
                "user_id": event_dict["user_id"],
                "body": event_dict["body"],
            }
        ),
        code,
    )
