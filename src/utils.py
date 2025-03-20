import requests
from urllib.parse import urlparse, parse_qs
from requests.cookies import cookiejar_from_dict
from config import headers, options_headers, comment_url

class ClientPool:
    def __init__(self, cookies):
        self.pool = []
        for cookie in cookies:
            jar = cookiejar_from_dict({c.strip().split('=')[0]: c.strip().split('=')[1] for c in cookie.split(';')})
            session = requests.Session()
            session.cookies = jar
            session.headers.update(headers)
            self.pool.append(session)
        self.current_index = 0

    def get_client(self):
        client = self.pool[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.pool)
        return client

def init_client_pool(cookies):
    return ClientPool(cookies)

def fetch_comment_page(client, note_id, xsec_token, cursor):
    url = comment_url(note_id, cursor, xsec_token)
    response = client.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    if data.get('success'):
        return data.get('data')
    else:
        print(f"Error fetching comments: {data}")
        raise Exception(f"Error fetching comments: {data['msg']}")

def fetch_sub_comment_page(client, note_id, xsec_token, root_comment_id, cursor):
    url = f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page?note_id={note_id}&root_comment_id={root_comment_id}&num=10&cursor={cursor}&image_formats=jpg,webp,avif&top_comment_id=&xsec_token={xsec_token}"
    response = send_options_request(client, url)
    response = client.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    if data.get('success'):
        return data.get('data')
    else:
        print(f"Error fetching sub-comments: {data}")
        raise Exception(f"Error fetching sub-comments: {data['msg']}")

def send_options_request(client, url):
    response = client.options(url, headers=options_headers)
    response.raise_for_status()
    new_cookies = response.headers.get('Set-Cookie')
    if new_cookies:
        for cookie in new_cookies.split(','):
            client.cookies.set(cookie.split('=')[0], cookie.split('=')[1].split(';')[0])
    return response

def extract_id_from_path(path):
    parts = path.split('/')
    for part in parts:
        if len(part) == 24 and all(c in '0123456789abcdef' for c in part):
            return part
    return None

def get_redirected_url(client, url):
    current_url = url
    max_redirects = 10
    for _ in range(max_redirects):
        response = client.head(current_url, allow_redirects=False)
        if 300 <= response.status_code < 400:
            current_url = response.headers['Location']
        else:
            return current_url
    raise Exception("Exceeded max redirects")

def get_url_params(client, url):
    parsed_url = urlparse(url)
    original_id = extract_id_from_path(parsed_url.path)
    original_token = parse_qs(parsed_url.query).get('xsec_token', [None])[0]

    if original_id and original_token:
        return original_id, original_token

    final_url = get_redirected_url(client, url)
    final_parsed = urlparse(final_url)
    final_id = extract_id_from_path(final_parsed.path)
    final_token = parse_qs(final_parsed.query).get('xsec_token', [None])[0]

    if not final_id or not final_token:
        print(f"链接访问不了 {final_id}, {final_token}")
        return final_id, final_token

    print(f"跟踪重定向 {final_id}, {final_token}")
    return final_id, final_token