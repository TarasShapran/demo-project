from djangochannelsrestframework.generics import GenericAsyncAPIConsumer


class ChatConsumer(GenericAsyncAPIConsumer):

    async def connect(self):
        if not self.scope['user']:
            await self.close()
        await self.accept()
