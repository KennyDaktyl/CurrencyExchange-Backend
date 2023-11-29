from django.utils import timezone


def local_time_str():
    local_time = timezone.localtime(timezone.now())
    return local_time.strftime("%Y-%m-%d %H:%M:%S")
