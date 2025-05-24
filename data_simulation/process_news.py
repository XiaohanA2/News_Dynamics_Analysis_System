import pandas as pd

news = pd.read_csv("./data/news.tsv", sep='\t', encoding='utf-8')

# 删去了无用字段Title entity和Entity content
news.drop(["Title entity", "Entity content"], axis=1, inplace=True)

# 重命名字段
news.rename(columns={
    "News ID": "news_id",
    "Category": "category",
    "Topic": "topic",
    "Headline": "headline",
    "News body": "content",
    }, inplace=True)

# 将news_id字段去除前导N，转换为int存储
news["news_id"] = news["news_id"].apply(lambda n: int(n[1:]) - 10000)

# 去除了换行符、制表符、转义符等无用数据
def etl_f(x):
    x = str(x)
    x = x.replace("\'", '').replace('\"', '')
    x = x.replace('"', '').replace("'", '')
    x = x.replace('\n', '').replace('\r', '').replace('\t', '')
    return x
news['category'] = news['category'].apply(lambda x: etl_f(x))
news['topic'] = news['topic'].apply(lambda x: etl_f(x))
news['headline'] = news['headline'].apply(lambda x: etl_f(x))
news['content'] = news['content'].apply(lambda x: etl_f(x))

news.to_csv("./processed_data/news.csv", index=False)