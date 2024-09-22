import csv
import os
import re

def read_csv_files():
    all_questions = []
    for i in range(1, 185):  # 讀取 book_1 到 book_184
        filename = f'book_{i}.csv'
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0].isdigit():  # 確保第一個欄位是數字
                        all_questions.append(row)
    return all_questions

def sort_questions(questions):
    return sorted(questions, key=lambda x: int(x[0]))

def clean_question_text(text):
    # 移除開頭的 1-10 加頓號，以及所有空白
    cleaned_text = re.sub(r'^([1-9]|10)、\s*', '', text)
    # 移除所有空白字符
    cleaned_text = re.sub(r'\s+', '', cleaned_text)
    return cleaned_text

def write_sorted_questions(questions):
    with open('book_all.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for question in questions:
            # 清理第二項（問題內容）
            if len(question) > 1:
                question[1] = clean_question_text(question[1])
            writer.writerow(question)

def check_and_fix_missing_numbers(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        questions = list(reader)

    last_number = int(questions[-1][0])
    fixed_questions = []
    current_number = 1

    for question in questions:
        question_number = int(question[0])
        while current_number < question_number:
            fixed_questions.append([str(current_number), "", "", "", "", "", ""])
            print(f"已插入缺失的題號: {current_number}")
            current_number += 1
        fixed_questions.append(question)
        current_number = question_number + 1

    if fixed_questions != questions:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(fixed_questions)
        print("檢查和修復完成")
    else:
        print("題號連續，無需修復")

def main():
    if not os.path.exists('book_all.csv'):
        print("book_all.csv 不存在，創建新文件...")
    else:
        print("book_all.csv 已存在，將被覆蓋...")

    all_questions = read_csv_files()
    sorted_questions = sort_questions(all_questions)
    write_sorted_questions(sorted_questions)
    print(f"排序完成，共處理 {len(sorted_questions)} 個問題。")
    print("結果已寫入 book_all.csv")

    # 檢查並修復缺失的題號
    check_and_fix_missing_numbers('book_all.csv')

if __name__ == "__main__":
    main()