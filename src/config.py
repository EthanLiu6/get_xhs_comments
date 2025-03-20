"""some config for your setting"""

# the cookie list for your web accounts
cookies = [
    # if your xhs account is disable or not login in, maybe backing:
    # {'code': -101, 'success': False, 'msg': '无登录信息，或登录信息为空', 'data': {}}
    # Error in get_comments: <Response [200]>
    'abRequestId=debcaf22-a1e2-5cb4-b059-846317c8c46c; webBuild=4.60.1; a1=195b3cbb3e5la48je7hv99es3e6joaawvd1wk8re530000594674; webId=3dcb239f6260041270093cd3bcdeb9b7; gid=yj2DqSDSy4hJyj2DqSDDqfYFd2104YVdWxhjyd2jdMqdKEq8Vl00ET8882j4KW48K82SJYWJ; web_session=040069b65bc54f24bcb9dd53e9354b03361393; xsecappid=xhs-pc-web; acw_tc=0ad585a917424877130714123e4c6596e664c07e61b8414556c53b26002a94; unread={%22ub%22:%2267d973e0000000001d020758%22%2C%22ue%22:%2267dc124c000000001d02c73c%22%2C%22uc%22:43}; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=19434595-8453-4efa-b6b1-3c2282c4bf89; loadts=1742488399591'
    ]


def comment_url(note_id, cursor, xsec_token):
    return f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={note_id}&cursor={cursor}&top_comment_id=&image_formats=jpg,webp,avif&xsec_token={xsec_token}"


# Headers
headers = {
    'authority': 'edith.xiaohongshu.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    # if IP has forbidden, please set a new 'user-agent'
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
}

options_headers = {
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': '*/*',
    'access-control-request-method': 'GET',  # CORS 预检专用头
    'access-control-request-headers': 'x-b3-traceid,x-mns,x-s,x-s-common,x-t,x-xray-traceid',  # CORS 预检专用头
    'origin': 'https://www.xiaohongshu.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.xiaohongshu.com/',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'priority': 'u=1, i'
}

# note_list: the web urls of xhs notes that you can get
note_list = [

]

# output path for your data files
output_path = '../output/'
