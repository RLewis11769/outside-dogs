""" Helper functions for user app """


def get_profile_pic(self):
    """ Return profile pic filepath """
    return f'profile_images/{self.id}/{"profile_pic.png"}'


def get_default_profile_pic():
    """ Return default profile pic filepath """
    return f'profile_images/default_pic.png'


def get_redirect_destination(request):
    """ Get redirect destination from query string if exists """
    redirect = None
    # Check if request exists and if parameter 'next' is in request
    if request.GET and request.GET.get('next'):
        redirect = str(request.GET.get('next'))
    return redirect
