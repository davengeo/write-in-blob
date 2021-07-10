import logging
from urllib import parse
from typing import Any, Tuple

from dependency_injector.wiring import Provide
from devopstoolsdaven.reports.report import Report
from devopstoolsdaven.vault.vault import Vault
from kombu import Message
from messagehandler.message_handler import MessageHandler


class BlobWriterHandler(MessageHandler):

    def __init__(self, service_url: str,
                 vault: Vault = Provide['vault_service'],
                 report: Report = Provide['report_service']) -> None:
        self.__service = service_url
        self.__origin = ''
        self.__vault = vault
        self.__report = report

    def setup(self, params: Tuple[Any, ...]) -> None:
        print(parse.urlparse(self.__service).netloc)

    def handler(self, body: Any, message: Message) -> None:
        logging.debug('received from {}: {}'.format(self.__origin, str(body)))
        if self.__report is not None:
            self.__report.add_event_with_type(event_type='message received',
                                              record={
                                                  'from_queue': self.__origin,
                                                  'message': body
                                              })
        message.ack()
