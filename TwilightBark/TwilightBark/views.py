""" Views aka url/html not associated with any other app """
from django.shortcuts import render


def index(response):
    """ Defines home page """
    return render(response, 'TwilightBark/index.html', {})
