import pandas as pd
import multiprocessing
import os
import numpy as np
from tqdm import tqdm
import gc

def process_chunk(chunk_info):
    """处理数据块的函数"""
    start, end, file_path = chunk_info
    
    try:
        # 只读取需要的行，减少内存使用
        # 使用低内存模式读取CSV
        logdata = pd.read_csv(
            file_path, 
            skiprows=range(1, start+1) if start > 0 else None,
            nrows=end-start,
            low_memory=True
        )
        
        # 创建一个空列表来存储结果行，比直接操作DataFrame更高效
        result_rows = []
        
        # 使用更高效的迭代方式
        for _, row in tqdm(logdata.iterrows(), total=len(logdata), 
                          desc=f"Processing {start}-{end}", ncols=80):
            user_id = int(row['UserID'])
            news_id_list = row['ClicknewsID'].split(' ')
            duration_list = row['dwelltime'].split(' ')
            start_timestamp_list = row['exposure_time'].split(' ')
            
            for i in range(len(news_id_list)):
                try:
                    news_id = int(news_id_list[i][1:]) - 10000
                    duration_time = int(duration_list[i])
                    start_timestamp = int(start_timestamp_list[i])
                    result_rows.append([user_id, news_id, start_timestamp, duration_time])
                except (IndexError, ValueError) as e:
                    # 处理可能的数据错误
                    print(f"Error processing data at row {_}, index {i}: {e}")
                    continue
        
        # 一次性创建DataFrame，而不是逐行添加
        df = pd.DataFrame(result_rows, columns=['user_id', 'news_id', 'start_ts', 'duration'])
        
        # 确保输出目录存在
        os.makedirs("./logcsvs", exist_ok=True)
        
        # 保存处理结果
        df.to_csv(f"./logcsvs/userid_{start}_{end}.csv", index=False)
        
        # 手动清理内存
        del logdata, df, result_rows
        gc.collect()
        
        return f"Chunk {start}-{end} processed, {len(result_rows)} lines generated"
    
    except Exception as e:
        return f"Error processing chunk {start}-{end}: {str(e)}"

def get_file_line_count(file_path):
    """获取文件的行数"""
    with open(file_path, 'r') as f:
        return sum(1 for _ in f)

def main():
    # 文件路径
    file_path = "./processed_data/single_userid_log.csv"
    
    # 获取文件总行数（不加载整个文件到内存）
    print("Counting file lines...")
    total_rows = get_file_line_count(file_path) - 1  # 减去标题行
    print(f"Total rows: {total_rows}")
    
    # 确定CPU核心数，但限制最大进程数以避免内存过载
    num_cores = min(multiprocessing.cpu_count(), 4)  # 最多使用4个核心
    print(f"Using {num_cores} CPU cores")
    
    # 计算每个进程处理的数据块大小
    chunk_size = total_rows // num_cores
    if chunk_size == 0:
        chunk_size = 1
    
    # 创建数据块范围列表
    chunks = []
    for i in range(0, total_rows, chunk_size):
        end = min(i + chunk_size, total_rows)
        chunks.append((i, end, file_path))
    
    # 创建进程池并执行处理
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(process_chunk, chunks)
    
    # 打印处理结果
    for result in results:
        print(result)
    
    print("All processing complete!")

if __name__ == "__main__":
    # 设置pandas显示选项，减少内存使用
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    
    # 启动主程序
    main()
