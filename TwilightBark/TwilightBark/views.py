from django.shortcuts import render


def index(response):
	""" Defines home page """
	return render(response, 'TwilightBark/index.html', {})
