package cn.edu.tongji.bi.repository;

import cn.edu.tongji.bi.entity.TNewsDailyCategoryEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface NewsDailyCategoryRepository extends JpaRepository<TNewsDailyCategoryEntity, Long> {
    @Query("SELECT ndc.dayStamp, ndc.category, ndc.browseCount " +
           "FROM TNewsDailyCategoryEntity ndc " +
           "WHERE ndc.dayStamp BETWEEN :startDay AND :endDay " +
           "AND ndc.category IN :categories " +
           "GROUP BY ndc.dayStamp, ndc.category")
    List<Object[]> findCategoryNewsChanging(@Param("categories") List<String> categories,
                                          @Param("startDay") Long startDay,
                                          @Param("endDay") Long endDay);
} 