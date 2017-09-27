# coding: utf: 8


def pretty_date(time=False):  # noqa
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:  # future
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return f'{second_diff} seconds ago'
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return f'{round(second_diff / 60):.0f} minutes ago'
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return f'{round(second_diff / 3600):.0f} hours ago'
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return f'{day_diff} days ago'
    if day_diff < 31:
        return f'{round(day_diff / 7):.0f} weeks ago'
    if day_diff < 365:
        return f'{round(day_diff / 30):.0f} months ago'
    return f'{round(day_diff / 365):.0f} years ago'


if __name__ == "__main__":
    from datetime import timedelta, datetime
    pp = pretty_date
    now = datetime.now()

    print(pp(now - timedelta(hours=18)))
    print(pp(now - timedelta(minutes=18)))
    print(pp(now - timedelta(seconds=18)))
    print(pp(now - timedelta(seconds=58)))

    print(pp(now - timedelta(days=200)))
    print(pp(now - timedelta(days=365)))
    print(pp(now - timedelta(days=367)))
    print(pp(now - timedelta(days=600)))
    print(pp(now - timedelta(days=1200)))
    print(pp(now - timedelta(days=12000)))

    print(pp(now - timedelta(days=31)))
    print(pp(now - timedelta(days=30)))

    print(pp(now - timedelta(days=20)))
    print(pp(now - timedelta(days=8)))
    print(pp(now - timedelta(days=7)))
    print(pp(now - timedelta(days=4)))
    print(pp(now - timedelta(days=1)))
    print(pp(now + timedelta(days=1)))
    print(pp(now - now))
    print(pp())
