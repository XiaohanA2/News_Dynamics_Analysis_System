from kafka import KafkaConsumer
import mysql.connector
from datetime import datetime
import json

# Kafka 配置
KAFKA_TOPIC = 'flume-topic'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# MySQL 配置
DB_CONFIG = {
    'host': '******',
    'user': '******',
    'password': '******',
    'database': 'pens_db',
}

# 初始化 Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='news-etl-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

# 建立 MySQL 连接
db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

print("⏳ 正在监听 Kafka 消息...")

try:
    for message in consumer:
        line = message.value.strip()

        try:
            # 解析 CSV 行
            parts = line.split(' ')
            if len(parts) != 4:
                print("⚠️ 数据格式不正确，跳过")
                continue

            user_id = int(parts[0])
            news_id = int(parts[1])
            start_ts = int(parts[2])
            duration = int(parts[3])
            start_day = start_ts // 86400 + 1

            # 1. 查询新闻的 category
            cursor.execute("SELECT category FROM t_news WHERE news_id = %s", (news_id,))
            result = cursor.fetchone()
            if not result:
                print(f"⚠️ 找不到新闻 {news_id} 的分类，跳过")
                continue
            category = result[0]

            # 2. 更新 t_news 表
            update_query = """
                UPDATE t_news
                SET total_browse_num = total_browse_num + 1,
                    total_browse_duration = total_browse_duration + %s
                WHERE news_id = %s
            """
            cursor.execute(update_query, (duration, news_id))

            # 3. 插入浏览记录
            insert_query = """
                INSERT INTO t_news_browse_record (user_id, news_id, start_ts, duration, start_day)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, news_id, start_ts, duration, start_day))

            # 4. 更新 t_news_daily_category 表（插入或更新）
            update_daily_category_query = """
                INSERT INTO t_news_daily_category (day_stamp, category, browse_count, browse_duration)
                VALUES (%s, %s, 1, %s)
                ON DUPLICATE KEY UPDATE
                    browse_count = browse_count + 1,
                    browse_duration = browse_duration + VALUES(browse_duration)
            """
            cursor.execute(update_daily_category_query, (start_day, category, duration))

            # 提交事务
            db.commit()

        except Exception as e:
            print(f"❌ 处理消息出错: {e}")
            db.rollback()

except KeyboardInterrupt:
    print("\n🛑 停止监听 Kafka")

finally:
    cursor.close()
    db.close()
    print("🔌 数据库连接已关闭")
