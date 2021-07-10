import os
import sys

from dependency_injector import containers, providers
from devopstoolsdaven.reports.logging_processor import init_logger_processor
from devopstoolsdaven.reports.report import init_report
from devopstoolsdaven.vault.vault_fake import VaultFake
from devopstoolsdaven.vault.vault_little import VaultLittle

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from writeinblob.write_in_blob import BlobWriterHandler  # noqa: E402


class TestContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    log_processor_service = providers.Resource(init_logger_processor,
                                               config_file=config.logging.config_file,
                                               logger=config.logging.logger,
                                               level=config.logging.level
                                               )
    processors_service = providers.List(log_processor_service, )
    report_service = providers.Resource(init_report,
                                        attributes=config.cloudevents,
                                        processors=processors_service)
    vault_service = providers.Selector(
        config.vault.implementation,
        json=providers.Singleton(VaultFake,
                                 path_json=config.vault.path_json),
        little=providers.Singleton(VaultLittle,
                                   url=config.vault.url,
                                   env=config.vault.env)
    )
    # noinspection Mypy
    blob_writer_service = providers.Factory(BlobWriterHandler,
                                            service_url=config.azure_blob.url,
                                            vault=vault_service,
                                            report=report_service
                                            )
