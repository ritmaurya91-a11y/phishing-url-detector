import re
from urllib.parse import urlparse

def extract_features(url):

    parsed = urlparse(url)

    # Feature 1: URL length
    url_length = len(url)

    # Feature 2: Number of dots
    dot_count = url.count(".")

    # Feature 3: HTTPS
    has_https = 1 if parsed.scheme == "https" else 0

    # Feature 4: IP address present
    ip_pattern = r"\d+\.\d+\.\d+\.\d+"
    has_ip = 1 if re.search(ip_pattern, url) else 0

    # Feature 5: Hyphen count
    hyphen_count = url.count("-")

    return [
        url_length,
        dot_count,
        has_https,
        has_ip,
        hyphen_count
    ]
