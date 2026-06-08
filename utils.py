import re
from urllib.parse import urlparse


def is_valid_url(url):
    pattern = re.compile(
        r'^(https?://)'
        r'([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.?)+'
        r'(\.[a-zA-Z]{2,})'
        r'(:[0-9]{1,5})?'
        r'(/[^\s]*)?$'
    )
    return bool(pattern.match(url.strip()))


def get_base_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def has_spaces(url):
    return ' ' in url


def is_too_long(url, max_length=200):
    return len(url) > max_length


def has_special_chars(url):
    parsed = urlparse(url)
    path = parsed.path
    decoded_path = re.sub(r'%[0-9A-Fa-f]{2}', '', path)
    bad = re.findall(r'[^a-zA-Z0-9\-._~/()]', decoded_path)
    return len(bad) > 0


def normalize_url(url):
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url
