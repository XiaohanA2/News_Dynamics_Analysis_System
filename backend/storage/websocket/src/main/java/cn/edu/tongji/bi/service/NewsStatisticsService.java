package cn.edu.tongji.bi.service;

import cn.edu.tongji.bi.entity.TNewsEntity;
import cn.edu.tongji.bi.entity.TNewsBrowseRecordEntity;
import cn.edu.tongji.bi.entity.TNewsDailyCategoryEntity;
import cn.edu.tongji.bi.repository.NewsRepository;
import cn.edu.tongji.bi.repository.NewsBrowseRecordRepository;
import cn.edu.tongji.bi.repository.NewsDailyCategoryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;

@Service
public class NewsStatisticsService {
    @Autowired
    private NewsRepository newsRepository;
    
    @Autowired
    private NewsBrowseRecordRepository newsBrowseRecordRepository;
    
    @Autowired
    private NewsDailyCategoryRepository newsDailyCategoryRepository;

    // 获取新闻标题模糊查询结果
    public List<Map<String, Object>> getHeadline(String headline, int amount) {
        List<TNewsEntity> news = newsRepository.findByHeadlineContaining(headline);
        List<Map<String, Object>> result = new ArrayList<>();
        
        for (TNewsEntity n : news) {
            Map<String, Object> item = new HashMap<>();
            item.put("news_id", n.getNewsId());
            item.put("headline", n.getHeadline());
            result.add(item);
        }
        
        return result.subList(0, Math.min(amount, result.size()));
    }

    // 获取单个新闻的生命周期数据
    public List<Map<String, Object>> getSingleNewsFashion(Long startTs, Long endTs, Long newsId) {
        List<Object[]> results = newsBrowseRecordRepository.findNewsFashion(startTs, endTs, newsId);
        List<Map<String, Object>> fashionData = new ArrayList<>();
        
        for (Object[] row : results) {
            Map<String, Object> item = new HashMap<>();
            item.put("count", row[0]);
            item.put("date", row[1]);
            fashionData.add(item);
        }
        
        return fashionData;
    }

    // 获取所有新闻类别
    public List<String> getAllCategories() {
        return newsRepository.findAllCategories();
    }

    // 获取某个类别的新闻变化情况
    public Map<String, List<Long>> getCategoryNewsChanging(List<String> categories, Long startTs, Long endTs) {
        Long startDay = startTs / 86400;
        Long endDay = Math.min(endTs / 86400, 18088L);
        
        List<Object[]> results = newsDailyCategoryRepository.findCategoryNewsChanging(
            categories, startDay, endDay);
        
        Map<String, List<Long>> result = new HashMap<>();
        for (String category : categories) {
            List<Long> counts = new ArrayList<>();
            for (long i = startDay; i <= endDay; i++) {
                counts.add(0L);
            }
            result.put(category, counts);
        }
        
        for (Object[] row : results) {
            String category = (String) row[1];
            Long dayStamp = (Long) row[0];
            Long count = (Long) row[2];
            result.get(category).set((int)(dayStamp - startDay), count);
        }
        
        return result;
    }

    // 获取用户兴趣变化
    public List<Map<String, Object>> getUserInterestChanging(Long userId, Long startTs, Long endTs) {
        List<Object[]> results = newsBrowseRecordRepository.findUserInterest(userId, startTs, endTs);
        List<Map<String, Object>> interestData = new ArrayList<>();
        
        for (Object[] row : results) {
            Map<String, Object> item = new HashMap<>();
            item.put("count", row[0]);
            item.put("category", row[1]);
            interestData.add(item);
        }
        
        return interestData;
    }

    // 获取新闻标题和内容的长度范围
    public Map<String, Object> getLengthRange() {
        Object[] result = newsRepository.findLengthRange();
        Map<String, Object> range = new HashMap<>();
        range.put("min_headline_length", result[0]);
        range.put("max_headline_length", result[1]);
        range.put("min_content_length", result[2]);
        range.put("max_content_length", result[3]);
        return range;
    }

    // 获取用户ID范围
    public Map<String, Long> getUserIdRange() {
        Object[] result = newsBrowseRecordRepository.findUserIdRange();
        Map<String, Long> range = new HashMap<>();
        range.put("min_user_id", (Long) result[0]);
        range.put("max_user_id", (Long) result[1]);
        return range;
    }

    // 通过类别获取主题
    public List<String> getTopicByCategory(String category) {
        return newsRepository.findTopicsByCategory(category);
    }

    // 获取新闻内容
    public String getContent(Long newsId) {
        return newsRepository.findContentByNewsId(newsId);
    }
} 