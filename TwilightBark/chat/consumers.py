""" Set up server-side consumer to handle backend websocket connections """
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import calculate_time, PayloadSerializer
from datetime import datetime
from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage
from django.core.paginator import Paginator
from math import ceil


class ChatConsumer(AsyncWebsocketConsumer):
    """ Consumer to asynchronously handle server websocket events """

    async def connect(self):
        """ Add user to room group and send message to group """

        # Find room"s group name so can connect users to it
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        try:
            # If room exists in db, get room object
            room = await get_room(self.room_name)
        except Exception as e:
            # If room doesn't exist in db, create room object
            room = await create_room(self.room_name)

        # Find user making connection request and add to db ChatRoom user list
        user = self.scope["user"]
        is_auth = user.is_authenticated
        if is_auth:
            await connect_user(room, user)

        # Add user to room group - group members receive messages from room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept all connections (even if not authenticated)
        await self.accept()

        # Get backlog of existing messages from db
        payload = await get_room_chat_messages(room)
        if payload:
            # Put into correct format for frontend
            payload = json.loads(payload)
            await self.send(text_data=json.dumps({
                # Only send message to self, not group
                "type": "load_messages",
                # Reverse dict to get messages in correct order oops
                # Note that messages contains data about each message, not just message text
                "messages": payload["messages"][::-1],
                "pageNum": payload["pageNum"]
            }))
        # Send message to room group - new user's name and new total user count
        total_users = get_num_users(room)
        await self.channel_layer.group_send(
            # Send message to everyone in room group
            self.room_group_name,
            {
                # Type connect_disconnect means pass params to connect_disconnect() function
                "type": "connect_disconnect",
                "user": user.username,
                "count": total_users,
                "event": "join"
            }
        )

    async def disconnect(self, close_code):
        """ Remove user from room group and send message to room group """

        # Find room_group_name to find who to send messages to
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Find user making disconnect request - remove from db if authenticated
        room = await get_room(self.room_name)
        user = self.scope["user"]
        is_auth = user.is_authenticated
        if is_auth:
            await disconnect_user(room, user)

        # Remove user from room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        total_users = get_num_users(room)
        await self.channel_layer.group_send(
            # Send message to all members of room group
            self.room_group_name,
            {
                "type": "connect_disconnect",
                "user": user.username,
                "count": total_users,
                "event": "leave"
            }
        )


    async def receive(self, text_data):
        """ Receive message from websocket frontend """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        if user.is_authenticated:
            # Only users can send messages - save to db and send to room group
            room = await get_room(self.room_name)
            if message:
                # Save message to db
                await create_message(room, user, message)
                # Send message to room group
                await self.channel_layer.group_send(
                    # type defines handler function to call
                    self.room_group_name,
                    {
                        "type": "create_chat_message",
                        # Message contains ONLY message text
                        "message": message,
                        "user": user.username,
                        # Pic to be set immediately
                        "pic": user.profile_pic.url,
                    }
                )
        else:
            # Anonymous users can't send messages
            await self.send(text_data=json.dumps({
                "msg_type": "error",
                "error": "You are not logged in"
            }))

    # Receive message from room group
    async def create_chat_message(self, event):
        message = event["message"]
        timestamp = calculate_time(datetime.now())

        await self.send(text_data=json.dumps({
            # Send message and data to frontend
            "msg_type": "message",
            "message": message,
            "user": event["user"],
            "timestamp": timestamp,
            "pic": event["pic"],
        }))

    async def connected_user_count(self, event):
        # Send number of users to frontend
        await self.send_json(
            {
                "msg_type": "count",
                "count": event["count"]
            },
        )

    async def connect_disconnect(self, event):
        """ Send message to room group based on event passed in connect() """
        join_leave = event["event"]
        await self.send(text_data=json.dumps({
            "msg_type": join_leave,
            "user": event["user"],
            "count": event["count"],
        }))


@database_sync_to_async
def create_room(name):
    """ Create new ChatRoom object in db based on name """
    return ChatRoom.objects.create(name=name)


@database_sync_to_async
def connect_user(room, user):
    """ ChatRoom method to connect user to room in many-to-many relationship """
    return room.connect_user(user)


@database_sync_to_async
def disconnect_user(room, user):
    """ ChatRoom method to remove user from many-to-many relationship """
    return room.disconnect_user(user)


@database_sync_to_async
def get_room(room_name):
    """ Return ChatRoom object from db based on name """
    try:
        room = ChatRoom.objects.get(name=room_name)
    except ChatRoom.DoesNotExist:
        raise Exception("Room does not exist")
    return room


@database_sync_to_async
def create_message(room, user, message):
    """ Create new ChatMessage object in db """
    return ChatMessage.objects.create(user=user, room=room, message=message)


def get_num_users(room):
    """ Find total number of users in ChatRoom """
    return len(room.users.all())


@database_sync_to_async
def get_room_chat_messages(room):
    """ Return all or one page of messages from db """
    try:
        # Get all messages in room
        qs = ChatMessage.objects.by_room(room)
        # Paginate queryset for number of messages per page (hardcoded as 5)
        paginator = Paginator(qs, 5)

        payload = {}
        if paginator.num_pages >= 1:
            # Use custom serializer to get messages in json format
            # messages are in reverse order so get page 1
            payload["messages"] = PayloadSerializer().serialize(paginator.page(1).object_list)
        else:
            payload["messages"] = "None"
        # Find last page if db has messages or else page 1
        payload["pageNum"] = ceil(paginator.count / 5) if paginator.count > 0 else 1
        # Put into json format in order to send back to consumer
        return json.dumps(payload)
    except Exception as e:
        print("EXCEPTION: " + str(e))
        return None
