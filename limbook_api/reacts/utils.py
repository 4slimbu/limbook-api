from random import randint

from limbook_api.reacts import React


def generate_react(user_id=None, post_id=None):
    """Generates new react with random attributes for testing
    """
    react = React(**{
        'user_id': user_id if user_id else str(randint(1000, 9999)),
        'post_id': post_id if post_id else randint(1000, 9999),
    })

    react.insert()
    return react
