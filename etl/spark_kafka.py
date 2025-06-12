from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, expr
import mysql.connector

# 初始化 Spark Session
spark = SparkSession.builder \
    .appName("KafkaNewsETL") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,mysql:mysql-connector-java:8.0.32") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 从 Kafka 读取数据
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "flume-topic") \
    .option("startingOffsets", "earliest") \
    .load()

# 提取消息并解析
lines = df.selectExpr("CAST(value AS STRING)").alias("line")

# 假设消息格式为：user_id news_id start_ts duration
fields = lines.select(split(col("value"), " ").alias("parts")) \
    .filter(expr("size(parts) = 4")) \
    .selectExpr(
        "CAST(parts[0] AS INT) AS user_id",
        "CAST(parts[1] AS INT) AS news_id",
        "CAST(parts[2] AS INT) AS start_ts",
        "CAST(parts[3] AS INT) AS duration"
    ) \
    .withColumn("start_day", expr("start_ts DIV 86400 + 1"))

# 定义用于将每行写入 MySQL 的函数
def write_to_mysql(batch_df, batch_id):
    # MySQL 配置
    conn = mysql.connector.connect(
        host="localhost",
        user="adminuser",
        password="123456",
        database="pens_db"
    )
    cursor = conn.cursor()

    for row in batch_df.collect():
        user_id, news_id, start_ts, duration, start_day = row

        try:
            # 查询 category
            cursor.execute("SELECT category FROM t_news WHERE news_id = %s", (news_id,))
            result = cursor.fetchone()
            if not result:
                print(f"⚠️ 找不到新闻 {news_id} 的分类，跳过")
                continue
            category = result[0]

            # 更新 t_news 表
            cursor.execute("""
                UPDATE t_news
                SET total_browse_num = total_browse_num + 1,
                    total_browse_duration = total_browse_duration + %s
                WHERE news_id = %s
            """, (duration, news_id))

            # 插入浏览记录
            cursor.execute("""
                INSERT INTO t_news_browse_record (user_id, news_id, start_ts, duration, start_day)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, news_id, start_ts, duration, start_day))

            # 更新 t_news_daily_category
            cursor.execute("""
                INSERT INTO t_news_daily_category (day_stamp, category, browse_count, browse_duration)
                VALUES (%s, %s, 1, %s)
                ON DUPLICATE KEY UPDATE
                    browse_count = browse_count + 1,
                    browse_duration = browse_duration + VALUES(browse_duration)
            """, (start_day, category, duration))

            conn.commit()
        except Exception as e:
            print(f"❌ 批次 {batch_id} 出错: {e}")
            conn.rollback()

    cursor.close()
    conn.close()

# 启动 Streaming Query，逐批处理
query = fields.writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_mysql) \
    .start()

query.awaitTermination()
