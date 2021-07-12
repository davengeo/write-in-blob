from uuid import uuid1


def build_blob_name(origin: str) -> str:
    return '{}-{}'.format(origin, str(uuid1()))
