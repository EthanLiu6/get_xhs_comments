import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

proxies = {
    "http": "http://proxy.example.com:8080",
    "https": "http://proxy.example.com:8080",
}

session = requests.Session()
retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
session.proxies.update(proxies)

def request_with_timestamp(method, url, **kwargs):
    headers = kwargs.get('headers', {})
    headers['x-timestamp'] = str(int(time.time() * 1000))
    kwargs['headers'] = headers
    response = session.request(method, url, **kwargs)
    duration = int(time.time() * 1000) - int(headers['x-timestamp'])
    print(f"请求耗时: {duration}ms")
    return response

session.request = request_with_timestamp