from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
import tomli
import tqdm
from flask_cors import CORS

with open("./config.toml", mode="rb") as fp:
    config = tomli.load(fp)

app = Flask(__name__)
CORS(app)
HOSTNAME = "100.81.9.75"
PORT = 3306
USERNAME = "hive"
PASSWORD = "shizb1207"
DATABASE = "bi_test"

db_config = config['database']
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
db = SQLAlchemy(app)


if __name__ == '__main__':
    start_day = 18060
    with app.app_context(), db.engine.connect() as conn:
        for start_day in tqdm.tqdm(range(18060, 18074)):
            sql = f"""
                INSERT INTO t_news_daily_category (
                    SELECT tnbr.start_day, n.category, count(tnbr.news_id), sum(tnbr.duration)
                    FROM (t_news_browse_record tnbr JOIN (SELECT news_id,category FROM t_news) AS n ON tnbr.news_id = n.news_id)
                    WHERE tnbr.start_day={start_day}
                    GROUP BY n.category
                );
                """
            try:
                res = conn.execute(text(sql))
                conn.commit()
            except Exception as e:
                print(e)
