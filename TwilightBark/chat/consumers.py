""" Set up server-side consumer (consumers have similar purpose to views) """
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import calculate_time
from datetime import datetime
from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    """ Consumer to asynchronously handle server websocket events """

    async def connect(self):
        """ Add user to room group and send message to group """

        # Find room's group name so can connect users to it
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        try:
            # If room exists in db, get room object
            room = await get_room(self.room_name)
        except Exception as e:
            # If room doesn't exist in db, create room object
            room = await create_room(self.room_name)

        # Find user making connection request and add to db ChatRoom user list
        user = self.scope['user']
        is_auth = user.is_authenticated
        if is_auth:
            await connect_user(room, user)

        # Store room_id in channel session for later use
        self.room_id = room.id

        # Add user to room group - group members receive messages from room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept all connections (even if not authenticated)
        await self.accept()

        # Send message to room group - new user's name and new total user count
        total_users = get_num_connected_users(room)
        await self.channel_layer.group_send(
            # Send message to everyone in room group
            self.room_group_name,
            {
                # Type who_connected means pass params to who_connected() below
                'type': 'who_connected',
                'user': user.username,
                'count': total_users
            }
        )

    async def who_connected(self, event):
        """ Send message to room group based on event passed in connect() """
        await self.send(text_data=json.dumps({
            "msg_type": "join",
            "user": event["user"],
            "count": event["count"]
        }))

    async def disconnect(self, close_code):
        """ Remove user from room group and send message to room group """

        # Find room_group_name to find who to send messages to
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        try:
            room = await get_room(self.room_name)
        except Exception as e:
            pass
        # Find user making disconnect request - remove from db if authenticated
        user = self.scope['user']
        is_auth = user.is_authenticated
        if is_auth:
            await disconnect_user(room, user)

        # Remove user from room group
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

        self.room_id = None

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
        if user.is_authenticated:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user.username
                }
            )
        else:
            await self.send(text_data=json.dumps({
                "msg_type": "error",
                "error": "You are not logged in"
            }))

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


def get_num_connected_users(room):
    return len(room.users.all())


@database_sync_to_async
def get_room(room_name):
    try:
        room = ChatRoom.objects.get(name=room_name)
    except ChatRoom.DoesNotExist:
        raise Exception("Room does not exist")
    return room
