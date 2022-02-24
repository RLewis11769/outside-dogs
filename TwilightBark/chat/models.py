""" Define models for chat room system - room and messages """
from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    """ Chat room model to hold Users and provide group for ChatMessages """
    name = models.CharField(max_length=100, unique=True, blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   help_text='Users connected to chat room')

    def __str__(self):
        """ String representation of chat room """
        return self.name

    def connect_user(self, user):
        """ When user connects to socket, add to chat room """
        is_user_added = False
        if user not in self.users.all():
            self.users.add(user)
            is_user_added = True
        if user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        """ When user disconnects from socket, remove from chat room """
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        """ Group name for socketio to subscribe to and send messages to """
        return f"ChatRoom-{self.id}"


class MessageManager(models.Manager):
    """ Message manager to return messages by room """

    def by_room(self, room):
        """ Get messages by room - ordered by latest first """
        queryset = ChatMessage.objects.filter(room=room).order_by('-timestamp')
        return queryset


class ChatMessage(models.Model):
    """ Chat message model for message created by User in ChatRoom """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField(unique=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Create interface between ChatMessage and ChatRoom
    objects = MessageManager()

    def __str__(self):
        """ String representation of chat message (content of message) """
        return self.message
