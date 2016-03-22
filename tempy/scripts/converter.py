import datetime


# Thanks to Fred Cirera
def human_readable_size(num, suffix='B'):
    for unit in [' ', ' Ki', ' Mi', ' Gi', ' Ti', ' Pi', ' Ei', ' Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_datetime():
    return datetime.datetime.now().strftime('%c')
