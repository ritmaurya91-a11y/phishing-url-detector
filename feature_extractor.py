import re
from urllib.parse import urlparse

def extract_features(url):
    return [
        1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else -1,
        1 if len(url) < 54 else -1,
        -1 if any(x in url for x in ["bit.ly","tinyurl","t.co","goo.gl"]) else 1,
        -1 if "@" in url else 1,
        -1 if url.rfind("//") > 6 else 1,
        -1 if "-" in urlparse(url).netloc else 1,
        -1 if urlparse(url).netloc.count(".") > 2 else 1,
        1 if url.startswith("https") else -1
    ]
