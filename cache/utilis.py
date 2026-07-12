import json
import os


CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")

os.makedirs(CACHE_DIR, exist_ok=True)


def get_cache_path(filename: str) -> str:
    return os.path.join(CACHE_DIR, filename)


def load_cache(filename : str) -> str:
    path = get_cache_path(filename)

    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}


def save_cache(filename : str, data : dict) -> str:
    path = get_cache_path(filename)

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def is_cache(filename: str, key: str) -> str:
    cache = load_cache(filename)
    return key in cache


def clear_cache(filename: str):
    path = get_cache_path(filename)

    if os.path.exists(path):
        os.remove(path)
        print("Cleared cache file")