import pandas as pd
from datetime import datetime
from tqdm import tqdm

train = pd.read_csv("./data/train.tsv", sep='\t')
valid = pd.read_csv("./data/valid.tsv", sep='\t')

 # 合并train和valid
logdata = pd.concat([train, valid], axis=0)

# 去除UserID的前导U，并转换为int
logdata['UserID'] = logdata['UserID'].apply(lambda x: int(x[1:]))

# 将start和end字段转换为时间戳
logdata['start'] = logdata['start'].apply(lambda str_t: int(datetime.strptime(str_t, '%m/%d/%Y %I:%M:%S %p').timestamp()))
logdata['end'] = logdata['end'].apply(lambda str_t: int(datetime.strptime(str_t, '%m/%d/%Y %I:%M:%S %p').timestamp()))

# 将诸如 【6/19/2019 5:10:01 AM#TAB#6/19/2019 5:11:58 AM】 的字段以#TAB拆分，并转换为时间戳
def f1(str_t):
    str_t_list = str_t.split('#TAB#')
    timestamp_list = list(map(lambda str_t: str(int(datetime.strptime(str_t, '%m/%d/%Y %I:%M:%S %p').timestamp())), str_t_list))
    return ' '.join(timestamp_list)
logdata['exposure_time'] = logdata['exposure_time'].apply(lambda str_t: f1(str_t))

# 去除冗余的UserID行
logdata = logdata.sort_values('UserID', ascending=True)
logdata = logdata.drop_duplicates(subset='UserID', keep='last')
logdata.to_csv("./processed_data/single_userid_log.csv", index=False)
