![image](https://user-images.githubusercontent.com/30398606/179889758-a2172247-50a0-405d-bc23-66f8d599169c.png)

Spring配置文件bootstrap.yml中设置nacos配置，出现错误。

应该是编码问题，修改IDEA的编码：
![image](https://user-images.githubusercontent.com/30398606/179895323-4404ef4b-31ca-4518-92b6-a67f89f39d17.png)

或者
#TODO

bat file:
chcp 65001
java -Dfile.encoding=utf-8 -jar XXXX.jar
Thanks for reply.I found a more effective way was add a system environment variable for maven:
JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF-8

https://github.com/alibaba/spring-cloud-alibaba/issues/1200
