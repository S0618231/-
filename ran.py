import subprocess
import sys
from datetime import datetime, time
import pytz

def check_time():
    taiwan_tz = pytz.timezone('Asia/Taipei')
    current_time = datetime.now(taiwan_tz).time()
    end_time = time(10, 0)  # 10:00 AM
    return current_time >= end_time

def run_script(script_name, bookID):
    print(f"執行腳本，輸入 BookID: {bookID}")
    subprocess.run([sys.executable, script_name, str(bookID)])

def main():
    script_to_run = "app.py"  # 您要運行的腳本名稱
    
    for i in range(1, 3, 1):
        if check_time():
            print("已到達結束時間（台灣時間 10:00），程序結束。")
            break
        
        bookID = i  # 這裡可以根據需要調整 BookID 的計算方式
        print(f"\n--- 執行第 {i} 次，BookID: {bookID} ---")
        run_script(script_to_run, bookID)
        print("--- 腳本執行完畢 ---")

    print("\n所有執行已完成")

if __name__ == "__main__":
    main()