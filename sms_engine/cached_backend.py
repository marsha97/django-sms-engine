from django.conf import settings
from django.core.cache import cache

from sms_engine.models import Backend


if hasattr(settings, 'TEST') and settings.TEST:
    CACHE_KEY = 'test:backend'
else:
    CACHE_KEY = 'backend'


def delete():
    key = CACHE_KEY
    cache.delete(key)


def get(use_cache=True):
    """ Get backend aliases as a dictionary which are cached by defaults.
    """
    key = CACHE_KEY
    #  Type Dict[int, List[str]] 
    backend_dict = {}

    if cache:
        # Hit cache first
        backend_aliases = cache.get(key)
        if backend_aliases:
            return backend_aliases

    # Cache miss, build the dict
    backend_dict = {
        Backend.PRIORITY.high: [],
        Backend.PRIORITY.normal: [],
        Backend.PRIORITY.low: [],
    }
    backends = Backend.objects.filter(is_active=True).order_by('priority', 'id')
    for backend in backends:
        backend_dict[backend.priority].append(backend.alias)

    if use_cache:
        cache.set(key, backend_dict)
    return backend_dict
