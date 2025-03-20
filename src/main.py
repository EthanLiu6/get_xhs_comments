import time
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import cookies, note_list, output_path
from csv_tool import save_comments_csv, get_unique_file_path
from utils import init_client_pool, fetch_comment_page, get_url_params

# 爬取间隔
duration_note = 0.5  # 主贴
duration_comment = 1.5  # 评论
duration_subcomment = 1.5  # 子评论

# 保存数据
page = 100
c_list = []
csv_file_path = get_unique_file_path(output_path + './comments.csv')

# 初始化客户端池
pool = init_client_pool(cookies)


def handle_exit(sig, frame):
    print('程序中断，保存已获取的数据...')
    if c_list:
        save_comments_csv(c_list, csv_file_path)
        print('保存剩余评论', len(c_list))
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)


def get_comments(client, note_id, xsec_token, cursor='', total_comments=0):
    page_comment_count = 0

    def handle_response(response):
        nonlocal page_comment_count
        nonlocal total_comments
        comments = response.get('comments', [])
        has_more = response.get('has_more', False)
        cursor = response.get('cursor', '')

        if not comments:
            print('未获取到评论数据或评论为空')
            return total_comments

        for comment in comments:
            comment['user_info'] = comment['user_info']['nickname']
            c_list.append(comment)

        page_comment_count = len(comments)
        total_comments += page_comment_count

        print(f"- 当前评论分页获取评论 {page_comment_count} 条，总计 {total_comments} 条")

        # 每次获取数据后立即保存
        save_comments_csv(c_list, csv_file_path)
        c_list.clear()

        if not has_more:
            return total_comments

        if page > 0:
            return get_comments(client, note_id, xsec_token, cursor, total_comments)
        else:
            print(f"已达到最大页数限制，笔记 {note_id} 共获取 {total_comments} 条评论")
            return total_comments

    try:
        time.sleep(duration_comment)
        response = fetch_comment_page(client, note_id, xsec_token, cursor)
        return handle_response(response)
    except Exception as e:
        print(f"Error in get_comments: {e}")
        return total_comments


def read_link(note_list, i):
    if i <= 0:
        if c_list:
            save_comments_csv(c_list, csv_file_path)
            print('所有链接处理完毕，保存剩余评论', len(c_list))
            c_list.clear()
        return

    client = pool.get_client()
    current_link = note_list[len(note_list) - i]
    note_id, xsec_token = get_url_params(client, current_link)
    link_comment_count = get_comments(client, note_id, xsec_token)
    print(f"链接 {current_link} 爬取完成，获取评论数: {link_comment_count}")

    read_link(note_list, i - 1)


def concurrent_read_links(note_list):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(read_link, note_list, i): i for i in range(1, len(note_list) + 1)}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Generated an exception: {e}")


if __name__ == '__main__':
    concurrent_read_links(note_list)

