package cn.edu.tongji.bi.repository;

import cn.edu.tongji.bi.entity.TNewsEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Map;


public interface NewsRepository extends JpaRepository<TNewsEntity, Integer> {
    @Query(value = "select news_id,category,topic,headline,content from t_news where category=(select category from t_news n join (select * from t_news_browse_record where user_id = ?1 order by start_ts desc limit 10)as r on n.news_id=r.news_id group by category order by count(*) desc limit 1) order by total_browse_num desc limit 10;", nativeQuery = true)
    List<Map<String,Object>> findNewsByUserId(int userId);

    @Query(value = "select t_news.news_id,t_news.headline,t_news.content,start_ts from t_news join (select * from t_news_browse_record where user_id = ?1 and start_ts>?2 order by start_ts desc limit 10)as j on j.news_id=t_news.news_id", nativeQuery = true)
    List<Map<String,Object>> getRecentClick(int userId,int startDay);

    List<TNewsEntity> findByHeadlineContaining(String headline);
    
    @Query("SELECT DISTINCT n.category FROM TNewsEntity n")
    List<String> findAllCategories();
    
    @Query("SELECT DISTINCT n.topic FROM TNewsEntity n WHERE n.category = :category")
    List<String> findTopicsByCategory(@Param("category") String category);
    
    @Query("SELECT MIN(LENGTH(n.headline)), MAX(LENGTH(n.headline)), " +
           "MIN(LENGTH(n.content)), MAX(LENGTH(n.content)) " +
           "FROM TNewsEntity n")
    Object[] findLengthRange();
    
    @Query("SELECT n.content FROM TNewsEntity n WHERE n.newsId = :newsId")
    String findContentByNewsId(@Param("newsId") Long newsId);
}
