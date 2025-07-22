import string
import random
import threading
from datetime import datetime
from urllib.parse import urlparse

class URLShortener:
    def __init__(self):
        self.url_map = {}
        self.clicks = {}
        self.created_at = {}
        self.lock = threading.Lock()
        self.code_length = 6
        self.allowed_chars = string.ascii_letters + string.digits

    def generate_short_code(self):
        while True:
            code = ''.join(random.choices(self.allowed_chars, k=self.code_length))
            with self.lock:
                if code not in self.url_map:
                    return code

    def is_valid_url(self, url):
        try:
            parsed = urlparse(url)
            return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
        except:
            return False

    def shorten_url(self, url):
        if not self.is_valid_url(url):
            raise ValueError("Invalid URL")

        with self.lock:
            for code, stored_url in self.url_map.items():
                if stored_url == url:
                    return code
            code = self.generate_short_code()
            self.url_map[code] = url
            self.clicks[code] = 0
            self.created_at[code] = datetime.utcnow()
            return code

    def get_original_url(self, short_code):
        with self.lock:
            return self.url_map.get(short_code)

    def increment_click(self, short_code):
        with self.lock:
            if short_code in self.clicks:
                self.clicks[short_code] += 1

    def get_stats(self, short_code):
        with self.lock:
            if short_code in self.url_map:
                return {
                    "url": self.url_map[short_code],
                    "clicks": self.clicks.get(short_code, 0),
                    "created_at": self.created_at[short_code].isoformat() + "Z"
                }
            return None
