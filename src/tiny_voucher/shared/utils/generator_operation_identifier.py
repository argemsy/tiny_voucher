# Standard Libraries
import uuid


def get_operation_id() -> str:
    return str(uuid.uuid4())
