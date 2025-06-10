from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from flask_cors import CORS
import tomli
from util import log
import time
import openai

with open("backend/storage/config.toml", mode="rb") as fp:
    config = tomli.load(fp)

app = Flask(__name__)
CORS(app)

db_config = config['database']
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
db = SQLAlchemy(app)

# 1、对单个新闻的生命周期的查询，可以展示单个新闻在不同时间段的流行变化

# 对headline进行模糊查询
@app.route('/news', methods=['GET'])
def getHeadline():
    data = request.args
    headline = data.get('headline')
    amount = data.get('amount')

    sql = f'''
        SELECT news_id,headline
        FROM t_news
        WHERE headline LIKE '%{headline}%'
        LIMIT {amount};
        '''
    start = time.time()
    with db.engine.connect() as conn:
        start = time.time()
        rows = conn.execute(text(sql)).fetchall()
        end = time.time()
        log(text(sql), end - start)
        result = [{'news_id': row.news_id, 'headline': row.headline} for row in rows]
        return jsonify(result)

# 获取某个新闻的生命周期
@app.route('/news/fashion', methods=['GET'])
def getSingleNewsFashion():
    data = request.args
    start_ts = data.get('start_ts')
    end_ts = data.get('end_ts')
    news_id = data.get('news_id')

    sql = f'''
        SELECT count(*), from_unixtime(tnbr.start_ts,"%Y-%m-%d")
        FROM t_news_browse_record tnbr
        WHERE {start_ts} <= tnbr.start_ts and tnbr.start_ts <= {end_ts} and news_id = {news_id}
        GROUP BY tnbr.news_id, from_unixtime(tnbr.start_ts,"%Y-%m-%d");
        '''

    with db.engine.connect() as conn:
        start = time.time()
        rows = conn.execute(text(sql)).fetchall()
        end = time.time()
        log(text(sql), end - start)
        result = [{'count': row[0], 'date': row[1]} for row in rows]
        return jsonify(result)


# 2、对某些种类的新闻的变化情况的统计查询，可以展示不同类别的

# 获取所有的新闻类别
@app.route('/category', methods=['GET'])
def getAllCategories():
    sql = f"""
        SELECT distinct(category)
        FROM t_news_daily_category;
        """
    with db.engine.connect() as conn:
        start = time.time()
        rows = conn.execute(text(sql)).fetchall()
        end = time.time()
        log(text(sql), end - start)
        result = [row[0] for row in rows]
        return jsonify(result)

# 获取某个类别的新闻的变化情况
@app.route('/news/category', methods=['GET'])
def getCategoryNewsChanging():
    data = request.args
    category = data.getlist('categorys[]')
    where_clause = ' or '.join([f"category = '{c}'" for c in category])
    start_ts = int(data.get('start_ts'))
    end_ts = int(data.get('end_ts'))
    start_day = start_ts // 86400
    end_day = min(end_ts // 86400, 18088)

    sql = f"""
        SELECT sum(tndc.browse_count), sum(tndc.browse_duration), tndc.day_stamp
        FROM t_news_daily_category tndc
        WHERE tndc.day_stamp>={start_day} and tndc.day_stamp<={end_day} and tndc.category = '{category}'
        GROUP BY tndc.day_stamp;
        """

    new_sql = f"""
        SELECT day_stamp, category, browse_count
        FROM t_news_daily_category WHERE day_stamp>={start_day} and day_stamp<={end_day} and ({where_clause})
        GROUP BY day_stamp, category;
        """

    with db.engine.connect() as conn:
        start = time.time()
        rows = conn.execute(text(new_sql)).fetchall()
        end = time.time()
        log(text(new_sql), end - start)
        result={}
        for row in rows:
            try:
                if(row[1] not in result):
                    result[row[1]] = []
                    for i in range(start_day,end_day+1):
                        result[row[1]].append(0)
                result[row[1]][int(row[0])-start_day] = row[2]
            except:
                print(row)
        return result


# 3、对用户兴趣变化的统计查询
@app.route('/user/interest', methods=['GET'])
def getUserInterestChanging():
    data = request.args
    user_id = data.get('user_id')
    start_ts = data.get('start_ts')
    end_ts = data.get('end_ts')
    
    sql = f"""
        SELECT count(*), n.category
        FROM
            t_news AS n
            JOIN (
                SELECT tnbr.news_id,tnbr.start_ts
                FROM t_news_browse_record AS tnbr
                WHERE tnbr.user_id={user_id} and tnbr.start_ts>={start_ts} and tnbr.start_ts<={end_ts}
            ) AS t ON n.news_id=t.news_id
        GROUP BY n.category;
        """
    with db.engine.connect() as conn:
        start = time.time()
        rows = conn.execute(text(sql)).fetchall()
        end = time.time()
        log(text(sql), end - start)
        # result = [{'count': row[0], 'category': row[1], 'date': row[2]} for row in rows]
        result = [{'count': row[0], 'category': row[1]} for row in rows]
        return jsonify(result)


# 4、可以按照时间/时间段、新闻主题（模糊匹配）、新闻标题长度、新闻长度、特定用户、特定多个用户等多种条件和组合进行统计查询

# 获取新闻标题、内容的长度范围
@app.route('/range/length', methods=['GET'])
def getLengthRange():
    sql = f"""
        SELECT min(user_id), max(user_id) FROM t_news_browse_record;
        """
    with db.engine.connect() as conn:
        sql = f"""
            SELECT min(length(headline)), max(length(headline)), min(length(content)), max(length(content))
            FROM t_news;
            """

        start = time.time()
        rows = conn.execute(text(sql)).fetchall()
        end = time.time()
        log(text(sql), end - start)
        row = rows[0]
        result = []
        result.append({'min_headline_length': row[0], 'max_headline_length': row[1], 'min_content_length': row[2], 'max_content_length': row[3]})
        return jsonify(result)

# 获取用户id的范围
@app.route('/range/userid', methods=['GET'])
def getUserIdRange():
    sql = f"""
        SELECT min(user_id), max(user_id) FROM t_news_browse_record;
        """

    with db.engine.connect() as conn:
        start = time.time()
        rows = conn.execute(text(sql)).fetchall()
        end = time.time()
        log(text(sql), end - start)
        result = [{'min_user_id': row[0], 'max_user_id': row[1]} for row in rows]
        return jsonify(result)

# 通过category获取topic
@app.route('/topic', methods=['GET'])
def getTopicByCategory():
    data = request.args
    category = data.get('category')
    sql = f"""
        SELECT DISTINCT(n.topic)
        FROM t_news n
        WHERE n.category='{category}';
        """

    with db.engine.connect() as conn:
        start = time.time()
        rows = conn.execute(text(sql)).fetchall()
        end = time.time()
        log(text(sql), end - start)
        result = [row[0] for row in rows]
        return jsonify(result)

# 通过newsid获取content
@app.route('/news/content', methods=['GET'])
def getContent():
    data = request.args
    news_id = data.get('news_id')
    sql = f"""
        SELECT n.content
        FROM t_news n
        WHERE n.news_id='{news_id}';
        """
    with db.engine.connect() as conn:
        start = time.time()
        rows = conn.execute(text(sql)).fetchall()
        end = time.time()
        log(text(sql), end - start)
        result = dict({"content":rows[0][0]}) 
        return result

# 组合查询
@app.route('/comprehensive', methods=['GET'])
def getConprehensiveInfo():
    data = request.args
    min_user_id = data.get('min_user_id')
    max_user_id = data.get('max_user_id')
    start_ts = data.get('start_ts')
    end_ts = data.get('end_ts')
    min_headline_length = data.get('min_headline_length')
    max_headline_length = data.get('max_headline_length')
    min_content_length = data.get('min_content_length')
    max_content_length = data.get('max_content_length')
    topic = data.get('topic')
    where_min_user_id = ""
    where_max_user_id = ""
    where_start_ts = ""
    where_end_ts = ""
    where_min_headline_length = ""
    where_max_headline_length = ""
    where_min_content_length = ""
    where_max_content_length = ""
    where_topic = ""
    temp = ""
    if start_ts:
        where_start_ts = f"tnbr.start_ts >= {start_ts}"
        temp = "and "
    if end_ts:
        where_end_ts = temp + f"tnbr.start_ts <= {end_ts}"
        temp = "and "
    if min_user_id:
        where_min_user_id = temp + f"user_id >= {min_user_id}"
        temp = "and "
    if max_user_id:
        where_max_user_id = temp + f"user_id <= {max_user_id}"
        temp = "and "
   
    temp2 = ""
    if min_headline_length:
        where_min_headline_length = f"LENGTH(n.headline) >= {min_headline_length} "
        temp2 = "and "
    if max_headline_length:
        where_max_headline_length = temp2 + f"LENGTH(n.headline) <= {max_headline_length}"
        temp2 = "and "
    if min_content_length:
        where_min_content_length = temp2 + f"LENGTH(n.content) >= {min_content_length}"
        temp2 = "and "
    if max_content_length:
        where_max_content_length = temp2 + f"LENGTH(n.content) <= {max_content_length}"
        temp2 = "and "
    if topic:
        where_topic = temp2 + f"n.topic like '%{topic}%'"

    sql = f"""
        SELECT DISTINCT new.headline, new.news_id
        FROM t_news_browse_record AS tnbr
            JOIN t_news AS new
            ON tnbr.news_id = new.news_id
        WHERE {where_start_ts} {where_end_ts} {where_min_user_id} {where_max_user_id} {temp} tnbr.news_id
            IN (
                SELECT news_id
                FROM t_news n
                WHERE {where_min_headline_length} {where_max_headline_length} {where_min_content_length} {where_max_content_length} {where_topic}
            );
        """
    with db.engine.connect() as conn:
        start = time.time()
        rows = conn.execute(text(sql)).fetchall()
        end = time.time()
        log(text(sql), end - start)
        result = [{'headline': row[0], 'news_id': row[1]} for row in rows]
        return jsonify(result)

# DeepSeek API 配置
DEEPSEEK_API_KEY = "sk-819fcb9cb98343eba13358c4b1613712"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

@app.route('/news/boom-analysis', methods=['POST'])
def news_boom_analysis():
    """
    输入：JSON，包含 category, topic, start_time, end_time
    输出：每条新闻的爆款概率和分析
    """
    data = request.json
    category = data.get('category')
    topic = data.get('topic')
    start_time = data.get('start_time')  # 例如 "2024-06-01 00:00:00"
    end_time = data.get('end_time')      # 例如 "2024-06-07 23:59:59"

    # 1. 查询新闻及统计数据
    sql = f"""
        SELECT n.news_id, n.headline, n.content, n.category, n.topic,
               COUNT(r.user_id) AS user_count, SUM(r.duration) AS total_duration
        FROM t_news n
        LEFT JOIN t_news_browse_record r ON n.news_id = r.news_id
        WHERE n.category = '{category}'
          AND n.topic = '{topic}'
          AND r.start_ts BETWEEN UNIX_TIMESTAMP('{start_time}') AND UNIX_TIMESTAMP('{end_time}')
        GROUP BY n.news_id
        LIMIT 1;
    """
    with db.engine.connect() as conn:
        start = time.time()
        rows = conn.execute(text(sql)).fetchall()
        end = time.time()
        news_list = []
        log(text(sql), end - start)
        for row in rows:
            news_list.append({
                "news_id": row.news_id,
                "headline": row.headline,
                "content": row.content,
                "category": row.category,
                "topic": row.topic,
                "user_count": row.user_count or 0,
                "total_duration": row.total_duration or 0
            })

    # 2. 调用 DeepSeek API 分析
    client = openai.OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    results = []
    for news in news_list:
        prompt = f"""
            新闻标题：{news['headline']}
            新闻内容：{news['content']}
            新闻类别：{news['category']}
            新闻主题：{news['topic']}
            用户数：{news['user_count']}
            浏览总时长：{news['total_duration']}
            分析问题：在{start_time}到{end_time}期间，这条新闻成为爆款新闻的概率有多大？请分析原因，并总结该时间段内爆款新闻的共同特征。
            """
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个资深数据分析师，擅长新闻爆款预测。"},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            analysis = response.choices[0].message.content
            print(news['headline'], time.time())
        except Exception as e:
            analysis = f"分析失败: {str(e)}"
        results.append({
            "news_id": news['news_id'],
            "headline": news['headline'],
            "analysis": analysis
        })

    return jsonify(results)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
