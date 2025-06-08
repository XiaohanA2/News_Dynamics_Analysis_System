package cn.edu.tongji.bi.controller;

import cn.edu.tongji.bi.service.NewsStatisticsService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(NewsStatisticsController.class)
public class NewsStatisticsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private NewsStatisticsService newsStatisticsService;

    @Test
    void testGetHeadline() throws Exception {
        // 准备测试数据
        Map<String, Object> news1 = new HashMap<>();
        news1.put("news_id", 1);
        news1.put("headline", "测试新闻1");
        Map<String, Object> news2 = new HashMap<>();
        news2.put("news_id", 2);
        news2.put("headline", "测试新闻2");
        List<Map<String, Object>> newsList = Arrays.asList(news1, news2);

        // 模拟Service行为
        when(newsStatisticsService.getHeadline("测试", 2)).thenReturn(newsList);

        // 执行测试
        mockMvc.perform(get("/api/news")
                .param("headline", "测试")
                .param("amount", "2"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].news_id").value(1))
                .andExpect(jsonPath("$[0].headline").value("测试新闻1"))
                .andExpect(jsonPath("$[1].news_id").value(2))
                .andExpect(jsonPath("$[1].headline").value("测试新闻2"));
    }

    @Test
    void testGetSingleNewsFashion() throws Exception {
        // 准备测试数据
        Map<String, Object> data1 = new HashMap<>();
        data1.put("count", 5);
        data1.put("date", "2020-09-13");
        Map<String, Object> data2 = new HashMap<>();
        data2.put("count", 3);
        data2.put("date", "2020-09-14");
        List<Map<String, Object>> fashionData = Arrays.asList(data1, data2);

        // 模拟Service行为
        when(newsStatisticsService.getSingleNewsFashion(1600000000L, 1600086400L, 1L))
            .thenReturn(fashionData);

        // 执行测试
        mockMvc.perform(get("/api/news/fashion")
                .param("startTs", "1600000000")
                .param("endTs", "1600086400")
                .param("newsId", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].count").value(5))
                .andExpect(jsonPath("$[0].date").value("2020-09-13"))
                .andExpect(jsonPath("$[1].count").value(3))
                .andExpect(jsonPath("$[1].date").value("2020-09-14"));
    }

    @Test
    void testGetAllCategories() throws Exception {
        // 准备测试数据
        List<String> categories = Arrays.asList("科技", "体育", "娱乐");

        // 模拟Service行为
        when(newsStatisticsService.getAllCategories()).thenReturn(categories);

        // 执行测试
        mockMvc.perform(get("/api/category"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0]").value("科技"))
                .andExpect(jsonPath("$[1]").value("体育"))
                .andExpect(jsonPath("$[2]").value("娱乐"));
    }

    @Test
    void testGetUserInterestChanging() throws Exception {
        // 准备测试数据
        Map<String, Object> interest1 = new HashMap<>();
        interest1.put("count", 10);
        interest1.put("category", "科技");
        Map<String, Object> interest2 = new HashMap<>();
        interest2.put("count", 5);
        interest2.put("category", "体育");
        List<Map<String, Object>> interestData = Arrays.asList(interest1, interest2);

        // 模拟Service行为
        when(newsStatisticsService.getUserInterestChanging(1L, 1600000000L, 1600086400L))
            .thenReturn(interestData);

        // 执行测试
        mockMvc.perform(get("/api/user/interest")
                .param("userId", "1")
                .param("startTs", "1600000000")
                .param("endTs", "1600086400"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].count").value(10))
                .andExpect(jsonPath("$[0].category").value("科技"))
                .andExpect(jsonPath("$[1].count").value(5))
                .andExpect(jsonPath("$[1].category").value("体育"));
    }
} 