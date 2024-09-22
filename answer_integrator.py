import csv
import logging
import os

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_csv(filename):
    data = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    try:
                        number = int(row[0])
                        answer = int(row[1])
                        data.append((number, answer))
                    except ValueError:
                        logging.warning(f"無法解析行: {row}")
                else:
                    logging.warning(f"行格式不正確: {row}")
    except FileNotFoundError:
        logging.error(f"{filename} 檔案不存在")
    return data

# 讀取 _ans.csv 檔案
input_data = read_csv('_ans.csv')

if not input_data:
    logging.error("無法從 _ans.csv 讀取資料或檔案為空")
    exit(1)

# 按題號排序資料
sorted_data = sorted(input_data, key=lambda x: x[0])

# 讀取現有的 ans.csv 檔案（如果存在）
existing_data = read_csv('ans.csv')

# 合併和更新資料
merged_data = {}
for number, answer in existing_data + sorted_data:
    merged_data[number] = answer

# 將合併後的資料轉換回列表並排序
final_data = sorted(merged_data.items())

# 將排序後的資料寫入 ans.csv
try:
    with open('ans.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(final_data)
    logging.info("處理完成。結果已寫入 ans.csv 檔案。")
except IOError:
    logging.error("無法寫入 ans.csv 檔案")

# 讀取 book_all.csv 檔案
book_all_data = []
try:
    with open('book_all.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        book_all_data = list(reader)
except FileNotFoundError:
    logging.warning("book_all.csv 檔案不存在。將創建新檔案。")

# 更新 book_all.csv
answer_dict = dict(final_data)
updated_book_all = []
answer_column_index = None

for row in book_all_data:
    if row:
        if answer_column_index is None:
            # 檢查是否已存在答案列
            for i, header in enumerate(row):
                if header.strip() == '答案':
                    answer_column_index = i
                    break
            
            # 如果沒有找到答案列，添加一個
            if answer_column_index is None:
                answer_column_index = len(row)
                row.append('答案')
        
        # 確保行的長度足夠
        while len(row) <= answer_column_index:
            row.append('')
        
        # 更新答案
        if int(row[0]) in answer_dict:
            row[answer_column_index] = str(answer_dict[int(row[0])])
    
    updated_book_all.append(row)

# 將更新後的資料寫入 book_all.csv
try:
    with open('book_all.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(updated_book_all)
    logging.info("處理完成。結果已寫入 book_all.csv 檔案。")
except IOError:
    logging.error("無法寫入 book_all.csv 檔案")

# 輸出一些統計資訊
logging.info(f"從 _ans.csv 讀取了 {len(input_data)} 條記錄")
logging.info(f"最終寫入 ans.csv 的記錄數: {len(final_data)}")
logging.info(f"更新了 book_all.csv 中的 {len([row for row in updated_book_all if row and row[answer_column_index]])} 條記錄")