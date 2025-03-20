import csv
import os


def get_unique_file_path(base_path):
    counter = 0
    file_path = base_path
    base_name, ext = os.path.splitext(base_path)
    while os.path.exists(file_path):
        counter += 1
        file_path = f"{base_name}.{counter}{ext}"
    return file_path


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def save_comments_csv(data, file_path, options={}):
    if not data:
        return
    # 动态生成字段名
    all_fieldnames = set()
    flattened_data = []
    for row in data:
        flat_row = flatten_dict(row)
        all_fieldnames.update(flat_row.keys())
        flattened_data.append(flat_row)
    fieldnames = list(all_fieldnames)

    file_exists = os.path.exists(file_path)

    with open(file_path, 'a', newline='', encoding=options.get('encoding', 'utf8')) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=options.get('delimiter', ','))
        if not file_exists:
            writer.writeheader()
        writer.writerows(flattened_data)
    print(f"CSV saved to: {file_path}")
    return True


def save_comments_csv2(data, file_path, options={}):
    if not data:
        return
    headers = [
        "u_user_id", "u_tenant_id", "u_platform", "u_ai_provider", "u_account_type",
        "u_identity_tags", "u_interest", "expand1", "expand2", "expand3", "expand4", "expand5",
        "type", "subtype", "sentiment", "neg_type", "keywords", "brands", "products",
        "content_type", "comm_type", "comm_reason", "comm_brand", "comment_id", "content",
        "platform", "score", "time", "like_count", "cls_type", "content_id", "parent_comment_id",
        "target_comment_id", "image_list", "user", "user_account", "sub_comment_count",
        "child_comment_count", "engagement_count", "post_user_replied", "post_user_replied_content",
        "prompt_personas", "suggested_response", "basic_suggested_response",
        "intermediate_suggested_response", "advanced_suggested_response", "process_status",
        "is_exception", "is_self", "content_info", "parent_content", "target_content",
        "staff_set_prompt_personas", "staff_upload_image_url", "staff_set_expect_liked_count",
        "staff_set_expect_publish_time", "exported_reply_crc32_list", "page_num", "page_position",
        "content_position", "possible_invalidation"
    ]

    file_exists = os.path.exists(file_path)

    with open(file_path, 'a', newline='', encoding=options.get('encoding', 'utf8')) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=options.get('delimiter', ','))
        if not file_exists:
            writer.writeheader()
        for row in data:
            for header in headers:
                if header not in row:
                    row[header] = None
            writer.writerow(row)
    print(f"CSV saved to: {file_path}")
    return True
