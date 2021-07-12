import json
import os
import sys
import time

from kombu import Message, Connection

from .mocks import Transport

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from writeinblob import write_in_blob  # noqa: E402
from .container import TestContainer  # noqa: E402

INI_PATH = '../app.ini'


def build_container() -> TestContainer:
    ct: TestContainer = TestContainer()
    ct.config.from_ini(os.path.join(os.path.dirname(__file__), INI_PATH))
    ct.wire(modules=[sys.modules[__name__], write_in_blob])
    ct.init_resources()
    return ct


def test_should_create_instance() -> None:
    ct = build_container()
    body: dict = {'test': 'messages'}
    write: write_in_blob.BlobWriterHandler = ct.blob_writer_service()
    write.setup(params=('from_test', ))
    write.handler(body=json.dumps(body),
                  message=Message(body=json.dumps(body),
                                  channel=Connection(transport=Transport).channel()))
    time.sleep(3)
    ct.shutdown_resources()
    time.sleep(3)
