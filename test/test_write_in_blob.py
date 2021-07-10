import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from writeinblob import write_in_blob   # noqa: E402
from .container import TestContainer    # noqa: E402

INI_PATH = '../app.ini'

ct: TestContainer = TestContainer()
ct.config.from_ini(os.path.join(os.path.dirname(__file__), INI_PATH))
ct.wire(modules=[sys.modules[__name__], write_in_blob])
ct.init_resources()


def test_should_create_instance() -> None:
    write: write_in_blob.BlobWriterHandler = ct.blob_writer_service()
    write.setup(params=())
    ct.shutdown_resources()
    time.sleep(3)
