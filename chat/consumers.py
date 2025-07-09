import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiver_username = self.scope['url_route']['kwargs']['username']
        self.sender = self.scope["user"]

        if self.sender.is_anonymous:
            await self.close()
        else:
            users = sorted([self.sender.username, self.receiver_username])
            self.room_name = f"{users[0]}_{users[1]}"
            self.room_group_name = f"chat_{self.room_name}"                                                                         

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"WebSocket Connected: {self.sender.username} to {self.room_group_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket Disconnected: {self.sender.username} from {self.room_group_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_username = self.sender.username
        receiver_username = self.receiver_username

        # print(f"Message received: {message} from {sender_username} to {receiver_username}")

        # Save message to DB
        await self.save_message(sender_username, receiver_username, message)

        # Broadcast to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, message):
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        Message.objects.create(sender=sender, receiver=receiver, content=message)
