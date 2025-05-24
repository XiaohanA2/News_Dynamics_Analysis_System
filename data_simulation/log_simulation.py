import time
import pandas as pd

logfile = pd.read_csv("./processed_data/log.csv")

current_timestamp = logfile.iloc[0]['start_ts']
for idx, row in logfile.iterrows():
    time.sleep(row['start_ts'] - current_timestamp)
    print(f"休眠了{row['start_ts'] - current_timestamp}秒") # sleep
    print(row.to_dict())
    with open("./click.log", "a") as f:
        f.write(" ".join(list(map(lambda x: str(x), row.to_list()))) + '\n')
    current_timestamp = row['start_ts']