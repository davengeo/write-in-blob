import json
from typing import Any, Tuple
from urllib import parse

from azure.storage.blob import BlobServiceClient, BlobClient
from dependency_injector.wiring import Provide, inject
from devopstoolsdaven.reports.report import Report
from devopstoolsdaven.vault.vault import Vault
from kombu import Message
from messagehandler.message_handler import MessageHandler

from .name_convention import build_blob_name


class BlobWriterHandler(MessageHandler):
    __origin: str = ''

    @inject
    def __init__(self, service_url: str, container: str,
                 vault: Vault = Provide['vault_service'],
                 report: Report = Provide['report_service']) -> None:
        self.__service: str = service_url
        self.__container: str = container
        self.__vault: Vault = vault
        self.__report: Report = report
        self.__blob_service: BlobServiceClient = BlobServiceClient.from_connection_string(
            self.__vault.read_secret(parse.urlparse(self.__service).netloc)['conn_string'])

    def setup(self, params: Tuple[Any, ...]) -> None:
        if len(params) < 1 or not isinstance(params[0], str):
            raise BadParamsException(params=params)
        self.__origin = params[0]

    def handler(self, body: Any, message: Message) -> None:
        self.__report.add_event_with_type(event_type='message received',
                                          record={
                                              'from_queue': self.__origin,
                                              'length': len(message.body),
                                              'headers': message.headers
                                          })
        blob_name: str = build_blob_name(origin=self.__origin)
        self.save_body(blob_name, message.body)
        self.save_headers(blob_name, message.headers)
        self.__report.add_event_with_type(event_type='message processed',
                                          record={
                                              'blob_name': blob_name,
                                              'service_url': self.__service,
                                              'container': self.__container
                                          })
        message.ack()

    def save_headers(self, blob_name: str, headers: dict) -> None:
        content: str = json.dumps(headers)
        client: BlobClient = self.__blob_service.get_blob_client(
            container=self.__container, blob='{}.headers'.format(blob_name))
        client.upload_blob(content, overwrite=True)
        client.close()

    def save_body(self, blob_name: str, body: str) -> None:
        client: BlobClient = self.__blob_service.get_blob_client(
            container=self.__container, blob='{}.body'.format(blob_name))
        client.upload_blob(body, overwrite=True)
        client.close()


class BadParamsException(ValueError):

    def __init__(self, params: Tuple[Any, ...]):
        self.__params = params

    def to_s(self) -> str:
        return ''.join(self.__params)
