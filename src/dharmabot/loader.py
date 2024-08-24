"""
The provided file contains a Python script that defines a function called `load_github_file` that fetches the raw content of a file from a GitHub URL and caches it based on a time duration. This caching mechanism helps in avoiding redundant requests for the same file within the specified time frame. The purpose of this script is to facilitate efficient loading and caching of GitHub files to improve performance and reduce unnecessary API calls in the context of DharmaBot UI.
"""

import functools
from functools import lru_cache
import time
import requests


CACHE_DURATION = 24 * 60 * 60


def time_based_cache(seconds):
    def wrapper_cache(func):
        func = lru_cache(maxsize=None)(func)
        func.lifetime = seconds
        func.expiration = time.time() + func.lifetime

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if time.time() >= func.expiration:
                func.cache_clear()
                func.expiration = time.time() + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


@time_based_cache(CACHE_DURATION)
def load_github_file(url):
    # Convert GitHub URL to raw content URL
    raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

    # Send a GET request to the raw URL
    response = requests.get(raw_url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to load file. Status code: {response.status_code}"
