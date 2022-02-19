""" Helper functions for user app """


def get_profile_pic(self):
    """ Return profile pic filepath """
    return f'profile_images/{self.id}/{"profile_pic.png"}'


def get_default_profile_pic():
    """ Return default profile pic filepath """
    return f'profile_images/default_pic.png'
