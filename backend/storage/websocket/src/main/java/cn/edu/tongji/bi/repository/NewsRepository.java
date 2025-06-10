package cn.edu.tongji.bi.repository;

import cn.edu.tongji.bi.entity.TNewsEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.Map;


public interface NewsRepository extends JpaRepository<TNewsEntity, Integer> {
    @Query(value = "select news.news_id,category,topic,headline,content from pens_db.t_news news join pens_db.t_news_current_popularity popular on news.news_id = popular.news_id where category=(select category from pens_db.t_news n join (select news_id from pens_db.t_news_browse_record where user_id = ?1 order by start_ts desc limit 10)as r on n.news_id=r.news_id group by category order by count(n.news_id) desc limit 1) order by popularity desc limit 10;", nativeQuery = true)
    List<Map<String,Object>> findNewsByUserId(int userId);
}
