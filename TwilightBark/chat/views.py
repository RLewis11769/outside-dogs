""" Define views connecting url to html template """
from django.shortcuts import render


def room(request, room_name):
    """ Define view for each room with room_name fron URL as context """
    return render(request, 'chat/room.html', {
        'room_name': room_name,
    })
