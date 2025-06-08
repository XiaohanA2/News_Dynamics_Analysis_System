package cn.edu.tongji.bi.repository;

import cn.edu.tongji.bi.entity.TNewsBrowseRecordEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface NewsBrowseRecordRepository extends JpaRepository<TNewsBrowseRecordEntity, Long> {
    @Query("SELECT COUNT(nbr), DATE_FORMAT(FROM_UNIXTIME(nbr.startTs), '%Y-%m-%d') " +
           "FROM TNewsBrowseRecordEntity nbr " +
           "WHERE nbr.startTs BETWEEN :startTs AND :endTs " +
           "AND nbr.newsId = :newsId " +
           "GROUP BY nbr.newsId, DATE_FORMAT(FROM_UNIXTIME(nbr.startTs), '%Y-%m-%d')")
    List<Object[]> findNewsFashion(@Param("startTs") Long startTs, 
                                 @Param("endTs") Long endTs, 
                                 @Param("newsId") Long newsId);
    
    @Query("SELECT COUNT(nbr), n.category " +
           "FROM TNewsBrowseRecordEntity nbr " +
           "JOIN TNewsEntity n ON nbr.newsId = n.newsId " +
           "WHERE nbr.userId = :userId " +
           "AND nbr.startTs BETWEEN :startTs AND :endTs " +
           "GROUP BY n.category")
    List<Object[]> findUserInterest(@Param("userId") Long userId,
                                  @Param("startTs") Long startTs,
                                  @Param("endTs") Long endTs);
                                  
    @Query("SELECT MIN(userId), MAX(userId) FROM TNewsBrowseRecordEntity")
    Object[] findUserIdRange();
} 