import hashlib
import threading

input_file = "input.txt"  # 包含原始数据的输入文件路径
output_file = "output.txt"  # 存储原始数据和 MD5 哈希值的输出文件路径
num_threads = 4  # 线程数

lock = threading.Lock()  # 创建锁对象，用于在多线程环境中安全地写入文件

# 处理单个原始数据的函数
def process_data(data):
    data_str = str(data)  # 将原始数据转换为字符串
    md5_hash = hashlib.md5(data_str.encode()).hexdigest()  # 计算 MD5 哈希值

    # 使用锁来保证多线程环境下写入文件的安全性
    with lock:
        with open(output_file, "a") as output:
            output.write(f"{data},{md5_hash}\n")  # 写入原始数据和 MD5 哈希值，逗号分隔

# 多线程处理原始数据
def process_data_thread(data_list):
    for data in data_list:
        process_data(data)

# 主程序
def main():
    with open(input_file, "r") as file:
        data_list = [line.strip() for line in file]  # 从输入文件中读取原始数据并存储为列表

    chunk_size = len(data_list) // num_threads  # 每个线程处理的原始数据数量

    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else len(data_list)
        chunk = data_list[start:end]

        thread = threading.Thread(target=process_data_thread, args=(chunk,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("加密完成！")

if __name__ == "__main__":
    main()
