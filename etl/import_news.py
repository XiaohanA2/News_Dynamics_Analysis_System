import pandas as pd
import pymysql

# 配置数据库连接
db_config = {
    'host': '121.40.162.87',
    'port': 3306,
    'username': 'adminuser',
    'password': '123456',
    'database': 'pens_db',
    'charset': 'utf8mb4'
}

# CSV 文件路径
csv_file = r'E:\商务智能\News_Dynamics_Analysis_System\data_simulation\processed_data\news.csv'

def import_csv_to_mysql(batch_size=1000):
    import math

    # 读取 CSV 文件
    df = pd.read_csv(csv_file)

    # 添加默认字段
    df['total_browse_num'] = 0
    df['total_browse_duration'] = 0

    # 重命名列以匹配表结构
    df = df[['news_id', 'headline', 'content', 'category', 'topic', 'total_browse_num', 'total_browse_duration']]

    # 替换 NaN 为 None（MySQL 可接受）
    df = df.where(pd.notnull(df), None)

    # 建立数据库连接
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    insert_sql = """
        INSERT INTO t_news (news_id, headline, content, category, topic, total_browse_num, total_browse_duration)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    try:
        total_rows = len(df)
        for i in range(0, total_rows, batch_size):
            batch_df = df.iloc[i:i+batch_size]
            batch_data = [tuple(row) for _, row in batch_df.iterrows()]
            cursor.executemany(insert_sql, batch_data)
            connection.commit()
            print(f"已插入第 {i + 1} 到 {min(i + batch_size, total_rows)} 条记录。")

        print("全部数据导入成功。")
    except Exception as e:
        connection.rollback()
        print("数据导入失败：", e)
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    import_csv_to_mysql()
