package cn.edu.tongji.bi.controller;

import cn.edu.tongji.bi.repository.NewsRepository;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.RestController;

import javax.websocket.*;
import javax.websocket.server.PathParam;
import javax.websocket.server.ServerEndpoint;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CopyOnWriteArraySet;

@RestController
@ServerEndpoint(value = "/websocket/{userid}")
@Component
public class WebSocketController {
    private int userid;

    private static CopyOnWriteArraySet<WebSocketController> webSocketControllerSet = new CopyOnWriteArraySet<>();

    private static NewsRepository newsRepository;
    private Session session = null;
    private static String path = "./query.log";
    @Autowired
    public void setUserService(NewsRepository newsRepository) {
        WebSocketController.newsRepository = newsRepository;
    }
    @OnOpen
    public void onOpen(Session session, @PathParam("userid") String userid) {
        // 建立连接
        this.session = session;
        webSocketControllerSet.add(this);
        this.userid = Integer.parseInt(userid);
    }

    @OnClose
    public void onClose() {
        // 关闭链接
        webSocketControllerSet.remove(this);
    }

    @OnMessage
    public void onMessage(String message, Session session) {
        for (WebSocketController item: webSocketControllerSet) {
            try {
                Map<String,Object> result = new HashMap<>(16);
                String sql = String.format("SELECT news_id, category, topic, headline, content FROM t_news WHERE category=(SELECT category FROM t_news n JOIN (SELECT * FROM t_news_browse_record WHERE user_id = %s ORDER BY start_ts DESC LIMIT 10) AS r ON n.news_id=r.news_id GROUP BY category ORDER BY count(*) DESC LIMIT 1) ORDER BY total_browse_num DESC LIMIT 10;", userid);
                Long startTime = System.currentTimeMillis();
                List<Map<String,Object>> news = newsRepository.findNewsByUserId(userid);
                Long endTime = System.currentTimeMillis();
                logSql(sql, (double)(endTime-startTime)/1000);
                result.put("news",news);
                item.session.getBasicRemote().sendText(JSON.toJSONString(result));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    @OnError
    public void onError(Session session, Throwable error) {
        error.printStackTrace();
    }

    private void logSql(String sql,Double time){
        String nowTime = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
        String log = String.format("[%s] %s %s" + "s",nowTime,sql,time);
        File file = new File(path);
        try {
            //追加写
            FileWriter fw = new FileWriter(file,true);
            PrintWriter pw = new PrintWriter(fw);
            pw.println(log);
            pw.flush();
            pw.close();
            fw.close();
        } catch (Exception e) {
            System.out.println(e.toString());
        }
    }
}
