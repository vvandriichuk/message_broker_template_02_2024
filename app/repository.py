class BrokerRepository:
    def __init__(self, broker):
        self.broker = broker

    async def listen_messages(self):
        return await self.broker.listen_messages()

    async def send_message(self, message):
        return await self.broker.send_message(message)

    async def delete_message(self, receipt_handle):
        return await self.broker.delete_message(receipt_handle)
