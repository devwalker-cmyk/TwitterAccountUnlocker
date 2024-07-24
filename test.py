import csv
import threading
import queue
from src.client import SessionManager

def check_token_and_update_status(token, result_queue):
    try:
        session_manager = SessionManager()
        status = session_manager.check_token(token)
    except Exception as e:
        status = f"Error: {e}"
    result_queue.put((token, status))

def worker( token_queue, result_queue):
    while True:
        token = token_queue.get()
        if token is None:
            break
        check_token_and_update_status(token, result_queue)
        token_queue.task_done()

def updater(file_path, result_queue):
    file_path = file_path.replace('.csv', '_new.csv')
    while True:
        token, status = result_queue.get()
        if token is None:
            break

        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([token, status])
        result_queue.task_done()

def main(file_path, num_threads):
    # session_manager = SessionManager([])
    token_queue = queue.Queue()
    result_queue = queue.Queue()

    # Đọc token từ file CSV và đẩy vào hàng đợi
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        tokens = [row[0] for row in reader]
        for token in tokens:
            token_queue.put(token)

    threads = []

    # Khởi tạo và chạy các luồng để kiểm tra token
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(token_queue, result_queue))
        threads.append(thread)
        thread.start()

    # Khởi tạo và chạy luồng để cập nhật file CSV
    update_thread = threading.Thread(target=updater, args=(file_path, result_queue))
    update_thread.start()

    # Chờ tất cả các tác vụ trong hàng đợi hoàn thành
    token_queue.join()

    # Đánh dấu kết thúc cho các luồng worker
    for _ in range(num_threads):
        token_queue.put(None)

    # Đợi tất cả các luồng worker hoàn thành
    for thread in threads:
        thread.join()

    # Đánh dấu kết thúc cho luồng updater
    result_queue.put((None, None))

    # Đợi luồng updater hoàn thành
    update_thread.join()




if __name__ == "__main__":
    file_path = input("Nhập đường dẫn file CSV: ")
    num_threads = int(input("Nhập số lượng luồng: "))

    main(file_path, num_threads)
