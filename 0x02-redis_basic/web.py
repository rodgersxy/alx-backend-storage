#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import redis
import requests
from typing import Callable
from functools import wraps

redis_client = redis.Redis()


def cache_and_count_requests(fn: Callable) -> Callable:
    """ Decorator wrapper """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper for decorator """
        try:
            redis_client.incr(f"count:{url}")
            cached_response = redis_client.get(f"cached:{url}")
            if cached_response:
                return cached_response.decode('utf-8')
            result = fn(url)
            redis_client.setex(f"cached:{url}", 10, result)
            return result
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return ""

    return wrapper


@cache_and_count_requests
def get_page(url: str) -> str:
    """Get page - self descriptive
    """
    response = requests.get(url)
    return response.text
