import subprocess
import sys
import multiprocessing
import os

def run_script(script_name, bookID):
    print(f"執行腳本，輸入 BookID: {bookID}")
    subprocess.run([sys.executable, script_name, str(bookID)])

def worker(start, end, script_to_run):
    for i in range(start, end):
        bookID = i
        print(f"\n--- 執行 BookID: {bookID} ---")
        run_script(script_to_run, bookID)
        print(f"--- BookID: {bookID} 執行完畢 ---")

def run_multi_process(script_to_run, start, end, num_processes):
    total_books = end - start + 1
    books_per_process = total_books // num_processes

    processes = []
    for i in range(num_processes):
        process_start = start + i * books_per_process
        process_end = process_start + books_per_process if i < num_processes - 1 else end + 1
        p = multiprocessing.Process(target=worker, args=(process_start, process_end, script_to_run))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

def main():
    script_to_run = "app.py"  # 您要運行的腳本名稱
    start_bookID = 31
    end_bookID = 60
    
    # 選擇執行模式
    use_multi_process = input("是否使用多進程執行？(y/n): ").lower() == 'y'
    
    if use_multi_process:
        num_processes = os.cpu_count()  # 使用 CPU 核心數量作為預設進程數
        custom_processes = input(f"請輸入進程數（預設為 {num_processes}，直接按 Enter 使用預設值）: ")
        if custom_processes:
            num_processes = int(custom_processes)
        
        print(f"\n使用 {num_processes} 個進程執行")
        run_multi_process(script_to_run, start_bookID, end_bookID, num_processes)
    else:
        for i in range(start_bookID, end_bookID + 1):
            bookID = i
            print(f"\n--- 執行第 {i} 次，BookID: {bookID} ---")
            run_script(script_to_run, bookID)
            print("--- 腳本執行完畢 ---")

    print("\n所有執行已完成")

if __name__ == "__main__":
    main()