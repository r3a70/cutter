

def convert_seconds_to_human_readable(seconds: int):

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
