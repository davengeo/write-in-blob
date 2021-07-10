import logging
from typing import Any, Tuple, Union

from devopstoolsdaven.reports.report import Report
from kombu import Message
from messagehandler.message_handler import MessageHandler


class TrivialHandler(MessageHandler):
    __report: Union[Report, None] = None
    __origin: Union[str, None] = None

    def setup(self, params: Tuple[Any, ...]) -> None:
        self.__origin = params[1]

    def handler(self, body: Any, message: Message) -> None:
        logging.debug('received from {}: {}'.format(self.__origin, str(body)))
        if self.__report is not None:
            self.__report.add_event_with_type(event_type='message received',
                                              record={
                                                  'from_queue': self.__origin,
                                                  'message': body
                                              })
        message.ack()
