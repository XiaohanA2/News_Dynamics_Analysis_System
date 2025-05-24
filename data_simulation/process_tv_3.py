import os, tqdm
import pandas as pd

# 合并并行得到的csv文件
his_csv_path = "./logcsvs"
csv_file_list = []
for filename in tqdm.tqdm(os.listdir(his_csv_path)):
    if filename.startswith('userid_'):
        csv_file = pd.read_csv(os.path.join(his_csv_path, filename))
        csv_file_list.append(csv_file)
cur_csv = pd.concat(csv_file_list, axis=0)

cur_csv = cur_csv.sort_values('start_ts', ascending=True)
cur_csv.to_csv("./processed_data/log.csv", index=False)