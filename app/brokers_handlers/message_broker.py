from abc import ABC, abstractmethod


class AbstractMessageBroker(ABC):
    @abstractmethod
    async def listen_messages(self):
        pass

    @abstractmethod
    async def send_message(self, message):
        pass

    @abstractmethod
    async def delete_message(self, receipt_handle):
        pass
