import csv
import os

input_folder = "../output/"  # 爬取的输出文件夹
output_file = "reduction01.csv"  # 输出格式化数据

# 目标数据格式列名
output_columns = ["index", "comment_id", "comment_text", "sentiment", "category", "response_text", "response_type"]

# 预定义情感类别
sentiment_categories = {
    "positive": "积极",
    "neutral": "中性",
    "negative": "消极"
}

# 预定义分类类别
comment_categories = {
    "suicidal": "轻生倾向",
    "work_stress": "工作/学业压力",
    "family_stress": "家庭压力",
    "social_anxiety": "社交焦虑",
    "appearance_anxiety": "容貌焦虑",
    "other": "其他"
}


# 读取所有 CSV 文件并转换格式
def process_data(input_folder, output_file):
    with open(output_file, "w", encoding="utf-8-sig", newline="") as outfile:
        writer = csv.writer(outfile)

        # 写入新表头
        writer.writerow(output_columns)

        index = 1  # 自增索引

        # 遍历文件夹内所有 CSV 文件
        for filename in os.listdir(input_folder):
            if filename.endswith(".csv"):  # 确保是 CSV 文件
                file_path = os.path.join(input_folder, filename)

                with open(file_path, "r", encoding="utf-8") as infile:
                    reader = csv.DictReader(infile)

                    for row in reader:
                        comment_id = row.get("id", "")
                        comment_text = row.get("content", "")

                        # 预设默认值
                        sentiment = "未标注"
                        category = "未分类"
                        response_text = ""
                        response_type = ""

                        # 写入新的 CSV 格式
                        writer.writerow(
                            [index, comment_id, comment_text, sentiment, category, response_text, response_type])
                        index += 1


if __name__ == '__main__':
    process_data(input_folder, output_file)
    print("数据转换完成，已保存至:", output_file)
