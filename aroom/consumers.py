import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    count = {}

    async def connect(self):
        print("connected")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        try:
            ChatConsumer.count.get(self.room_name)
            ChatConsumer.count[self.room_name] += 1
        except:
            ChatConsumer.count[self.room_name] = 1
        print(ChatConsumer.count)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'connections',
                'connected_user_count': ChatConsumer.count[self.room_name],
            }
        )
        

    async def disconnect(self, close_code):
        ChatConsumer.count[self.room_name] -= 1
        if ChatConsumer.count[self.room_name] == 0:
            ChatConsumer.count.pop(self.room_name)
        print("disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        if self.room_name in ChatConsumer.count:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'connections',
                    'connected_user_count': ChatConsumer.count[self.room_name]
                }
            )
    # Receive message from WebSocket
    async def receive(self, text_data):
        print("receiving data")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def connections(self, event):
        connections = event['connected_user_count']
        await self.send(text_data=json.dumps({
            'connected_user_count': connections
        }))


class PersonalChat(AsyncWebsocketConsumer):
    count = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        try:
            ChatConsumer.count.get(self.room_name)
            ChatConsumer.count[self.room_name] += 1
        except:
            ChatConsumer.count[self.room_name] = 1

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'connections',
                'connected_user_count': ChatConsumer.count[self.room_name],
            }
        )

    async def disconnect(self, close_code):
        print("disconnected")
        ChatConsumer.count[self.room_name] -= 1
        if ChatConsumer.count[self.room_name] == 0:
            ChatConsumer.count.pop(self.room_name)
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if self.room_name in ChatConsumer.count:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'connections',
                    'connected_user_count': ChatConsumer.count[self.room_name]
                }
            )


    async def receive(self, text_data):
        print("receiving data")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'personal_chat_message',
                'message': message,
                'connected_user_count': ChatConsumer.count[self.room_name]
            }
        )

    async def personal_chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'connected_user_count': ChatConsumer.count[self.room_name]
        }))

    async def connections(self, event):
        connections = event['connected_user_count']
        await self.send(text_data=json.dumps({
            'connected_user_count': connections
        }))