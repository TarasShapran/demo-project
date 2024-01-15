from channels.db import database_sync_to_async
from core.dataclasses.user_dataclass import UserDataClass
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from apps.chat.models import ChatModel


class ChatConsumer(GenericAsyncAPIConsumer):

    def __init__(self, *args, **kwargs):
        self.room_name = None
        self.user_name = None
        super().__init__(*args, **kwargs)

    async def connect(self):
        if not self.scope['user']:
            await self.close()
        await self.accept()
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.user_name = await self.get_profile_name()
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.send_last_five_msg()
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'body': f'connected to chat',
                'user': self.user_name
            }
        )

    async def sender(self, data):
        await self.send_json(data)

    @action()
    async def send_message(self, data, request_id, action):
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'body': data,
                'user': self.user_name,
                'id': request_id
            }
        )
        await self.save_msg_to_db(data, self.scope['user'])

    async def send_last_five_msg(self):
        messages = await self.get_last_five_msg()
        for msg in reversed(messages):
            await self.send_json(msg)

    @database_sync_to_async
    def get_profile_name(self):
        user: UserDataClass = self.scope['user']
        return user.profile.name

    @database_sync_to_async
    def save_msg_to_db(self, body, user):
        ChatModel.objects.create(body=body, user=user)

    @database_sync_to_async
    def get_last_five_msg(self):
        return [{'body': item.body, 'user': item.user.profile.name} for item in ChatModel.objects.order_by('id')[:5]]
