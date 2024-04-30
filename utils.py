from django.conf import settings
from django.core.cache import cache


def get_or_set_cache(key, callback, timeout=settings.DEFAULT_TTL):
    data = cache.get(key)
    if data is not None:
        return data
    else:
        data = callback()
        cache.set(key, data, timeout=timeout)
        return data
