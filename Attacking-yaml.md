参考：
- [Untrusted deserialization issue when loading newrelic.yml file in Java agent leads to code execution on host](https://hackerone.com/reports/1109620)
- [SnakeYaml反序列化不出网利用的思路](https://wx.zsxq.com/mweb/views/topicdetail/topicdetail.html?topic_id=218851115222111&inviter_id=28512258815451&share_from=ShareToWechat&keyword=RB2nUbu&d=46235497)
- https://www.mi1k7ea.com/2019/11/29/Java-SnakeYaml%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%BC%8F%E6%B4%9E/

第一步：利用 http://scz.617.cn:8/web/202008111715.txt 文中的链写jar文件
第二步：利用 Java SnakeYaml反序列化漏洞 [ Mi1k7ea ] ScriptEngineManager链 加载本地的jar文件

没记错的话，jdk1.6、1.7、1.8 都适用。
