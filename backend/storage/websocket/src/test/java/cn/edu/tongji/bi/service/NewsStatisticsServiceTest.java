package cn.edu.tongji.bi.service;

import cn.edu.tongji.bi.entity.TNewsEntity;
import cn.edu.tongji.bi.repository.NewsRepository;
import cn.edu.tongji.bi.repository.NewsBrowseRecordRepository;
import cn.edu.tongji.bi.repository.NewsDailyCategoryRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Arrays;
import java.util.List;
import java.util.Map;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class NewsStatisticsServiceTest {

    @InjectMocks
    private NewsStatisticsService newsStatisticsService;

    @Mock
    private NewsRepository newsRepository;

    @Mock
    private NewsBrowseRecordRepository newsBrowseRecordRepository;

    @Mock
    private NewsDailyCategoryRepository newsDailyCategoryRepository;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testGetHeadline() {
        // 准备测试数据
        String headline = "测试新闻";
        int amount = 10;
        List<Map<String, Object>> expectedResult = Arrays.asList(
            Map.of("news_id", 1, "headline", "测试新闻1"),
            Map.of("news_id", 2, "headline", "测试新闻2")
        );

        // 模拟Repository行为
        when(newsRepository.findByHeadlineContaining(headline)).thenReturn(
            Arrays.asList(
                createNewsEntity(1, "测试新闻1"),
                createNewsEntity(2, "测试新闻2")
            )
        );

        // 执行测试
        List<Map<String, Object>> result = newsStatisticsService.getHeadline(headline, amount);

        // 验证结果
        assertNotNull(result);
        assertEquals(expectedResult.size(), result.size());
        assertEquals(expectedResult.get(0).get("headline"), result.get(0).get("headline"));
    }

    @Test
    void testGetSingleNewsFashion() {
        // 准备测试数据
        int newsId = 1;
        Long startTs = 1609459200L; // 2021-01-01
        Long endTs = 1640995200L;   // 2022-01-01
        List<Object[]> expectedResult = Arrays.asList(
            new Object[]{10L, "2021-01-01"},
            new Object[]{15L, "2021-01-02"}
        );

        // 模拟Repository行为
        when(newsBrowseRecordRepository.findNewsFashion(startTs, endTs, Long.valueOf(newsId)))
            .thenReturn(expectedResult);

        // 执行测试
        List<Map<String, Object>> result = newsStatisticsService.getSingleNewsFashion(startTs, endTs, Long.valueOf(newsId));

        // 验证结果
        assertNotNull(result);
        assertEquals(expectedResult.size(), result.size());
        assertEquals(expectedResult.get(0)[0], result.get(0).get("count"));
    }

    @Test
    void testGetAllCategories() {
        // 准备测试数据
        List<String> expectedCategories = Arrays.asList("科技", "体育", "娱乐");

        // 模拟Repository行为
        when(newsRepository.findAllCategories()).thenReturn(expectedCategories);

        // 执行测试
        List<String> result = newsStatisticsService.getAllCategories();

        // 验证结果
        assertNotNull(result);
        assertEquals(expectedCategories.size(), result.size());
        assertEquals(expectedCategories, result);
    }

    @Test
    void testGetUserInterestChanging() {
        // 准备测试数据
        int userId = 1;
        Long startTs = 1609459200L; // 2021-01-01
        Long endTs = 1640995200L;   // 2022-01-01
        List<Object[]> expectedResult = Arrays.asList(
            new Object[]{10L, "科技"},
            new Object[]{15L, "体育"}
        );

        // 模拟Repository行为
        when(newsBrowseRecordRepository.findUserInterest(Long.valueOf(userId), startTs, endTs))
            .thenReturn(expectedResult);

        // 执行测试
        List<Map<String, Object>> result = newsStatisticsService.getUserInterestChanging(Long.valueOf(userId), startTs, endTs);

        // 验证结果
        assertNotNull(result);
        assertEquals(expectedResult.size(), result.size());
        assertEquals(expectedResult.get(0)[1], result.get(0).get("category"));
    }

    private TNewsEntity createNewsEntity(int newsId, String headline) {
        TNewsEntity news = new TNewsEntity();
        news.setNewsId(newsId);
        news.setHeadline(headline);
        return news;
    }
} 