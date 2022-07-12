```sh
wget https://archive.apache.org/dist/rocketmq/4.9.3/rocketmq-all-4.9.3-bin-release.zip
nohup sh bin/mqnamesrv &
```


启动之后，总是报错：
![image](https://user-images.githubusercontent.com/30398606/178466103-51f6ec7a-5990-4907-9380-fc469eeb0456.png)


![image](https://user-images.githubusercontent.com/30398606/178466034-8285f792-043f-49b8-b714-a1ef8a0ac2e3.png)
https://github.com/StyleTang/rocketmq-console-ng/blob/2b40f00023da3497ae33c59c2f4beff305011881/src/main/java/org/apache/rocketmq/console/task/DashboardCollectTask.java

查看配置文件：

![image](https://user-images.githubusercontent.com/30398606/178466506-afb15d0e-2c0f-47c8-ad7c-0b4b44fa0ae8.png)

最后将`@Scheduled`这个注解注释掉，重新编译。没有再报错了。
