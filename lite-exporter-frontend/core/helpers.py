class Section:
    def __init__(self, title, description, tiles):
        self.title = title
        self.description = description
        self.tiles = tiles


class Tile:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url


def generate_notification_string(notifications_count: int):
    if notifications_count == 0:
        return ''
    elif notifications_count == 1:
        return f'You have {notifications_count} new notification'
    else:
        return f'You have {notifications_count} new notifications'
