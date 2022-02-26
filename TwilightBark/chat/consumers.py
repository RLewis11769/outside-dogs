import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import calculate_time
from datetime import datetime
from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        try:
            room = await get_room(self.room_name)
        except Exception as e:
            room = await create_room(self.room_name)
        user = self.scope['user']
        is_auth = user.is_authenticated
        if is_auth:
            await connect_user(room, user)
        self.room_id = room.id
        # print(self.room_id)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Accept connection
        await self.accept()

        # Send message to room group
        total_users = get_num_connected_users(room)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'who_connected',
                'user': user.username,
                'count': total_users
            }
        )

    async def who_connected(self, event):
        await self.send(text_data=json.dumps({
            "msg_type": "join",
            "user": event["user"],
            "count": event["count"]
        }))

    async def disconnect(self, close_code):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        try:
            room = await get_room(self.room_name)
        except Exception as e:
            room = await create_room(self.room_name)
        user = self.scope['user']
        is_auth = user.is_authenticated
        if is_auth:
            await disconnect_user(room, user)
        self.room_id = None

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Send message to room group
        total_users = get_num_connected_users(room)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'who_left',
                'user': user.username,
                'count': total_users
            }
        )

        # # Get new total number of connected users
        # total_users = get_num_connected_users(room)
        # # Send message via connected_user_count to update the number of connected users
        # await self.channel_layer.group_send(
        #     room.group_name,
        #     {
        #         "type": "connected.user.count",
        #         "count": total_users,
        #     }
        # )

    async def who_left(self, event):
        await self.send(text_data=json.dumps({
            "msg_type": "leave",
            "user": event["user"],
            "count": event["count"]
        }))

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = self.scope['user']
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # user = self.scope['user']
        timestamp = calculate_time(datetime.now())

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'msg_type': "message",
            'message': message,
            'user': event["user"],
            'timestamp': timestamp
        }))

    async def connected_user_count(self, event):
        # Send message to frontend
        await self.send_json(
            {
                "msg_type": "count",
                "count": event["count"]
            },
        )


@database_sync_to_async
def connect_user(room, user):
    return room.connect_user(user)

@database_sync_to_async
def disconnect_user(room, user):
    return room.disconnect_user(user)

@database_sync_to_async
def create_room(name):
    return ChatRoom.objects.create(name=name)

# @database_sync_to_async
def get_num_connected_users(room):
    return len(room.users.all())

@database_sync_to_async
def get_room(room_name):
    try:
        room = ChatRoom.objects.get(name=room_name)
    except ChatRoom.DoesNotExist:
        raise Exception("Room does not exist")
    return room

