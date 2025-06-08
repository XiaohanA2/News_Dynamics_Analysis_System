package cn.edu.tongji.bi.controller;

import cn.edu.tongji.bi.service.NewsStatisticsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class NewsStatisticsController {
    @Autowired
    private NewsStatisticsService newsStatisticsService;

    // 新闻标题模糊查询
    @GetMapping("/news")
    public List<Map<String, Object>> getHeadline(
            @RequestParam String headline,
            @RequestParam(defaultValue = "10") int amount) {
        return newsStatisticsService.getHeadline(headline, amount);
    }

    // 获取单个新闻的生命周期
    @GetMapping("/news/fashion")
    public List<Map<String, Object>> getSingleNewsFashion(
            @RequestParam Long startTs,
            @RequestParam Long endTs,
            @RequestParam Long newsId) {
        return newsStatisticsService.getSingleNewsFashion(startTs, endTs, newsId);
    }

    // 获取所有新闻类别
    @GetMapping("/category")
    public List<String> getAllCategories() {
        return newsStatisticsService.getAllCategories();
    }

    // 获取某个类别的新闻变化情况
    @GetMapping("/news/category")
    public Map<String, List<Long>> getCategoryNewsChanging(
            @RequestParam List<String> categorys,
            @RequestParam Long startTs,
            @RequestParam Long endTs) {
        return newsStatisticsService.getCategoryNewsChanging(categorys, startTs, endTs);
    }

    // 获取用户兴趣变化
    @GetMapping("/user/interest")
    public List<Map<String, Object>> getUserInterestChanging(
            @RequestParam Long userId,
            @RequestParam Long startTs,
            @RequestParam Long endTs) {
        return newsStatisticsService.getUserInterestChanging(userId, startTs, endTs);
    }

    // 获取新闻标题和内容的长度范围
    @GetMapping("/range/length")
    public Map<String, Object> getLengthRange() {
        return newsStatisticsService.getLengthRange();
    }

    // 获取用户ID范围
    @GetMapping("/range/userid")
    public Map<String, Long> getUserIdRange() {
        return newsStatisticsService.getUserIdRange();
    }

    // 通过类别获取主题
    @GetMapping("/topic")
    public List<String> getTopicByCategory(@RequestParam String category) {
        return newsStatisticsService.getTopicByCategory(category);
    }

    // 获取新闻内容
    @GetMapping("/news/content")
    public Map<String, String> getContent(@RequestParam Long newsId) {
        return Map.of("content", newsStatisticsService.getContent(newsId));
    }
} 