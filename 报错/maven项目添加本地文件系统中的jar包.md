项目中碰到了`dubbo-2.5.4.1-SNAPSHOT`，
开始把`dubbo-2.5.4.1-SNAPSHOT`改成了官方仓库存在的`dubbo-2.5.4`，结果报这个错：

![image](https://user-images.githubusercontent.com/30398606/179917152-f5b68bfb-ae80-406a-b6b4-3ec43e0ccac9.png)

，于是下载[这个项目](https://github.com/zsj209/Dubbo)之后，编译，发布到本地：
```
mvn install:install-file -Dfile=C:\repos\Dubbo\dubbo\target\dubbo-2.5.4.1-SNAPSHOT.jar -DgroupId=com.alibaba -DartifactId=dubbo -Dversion=2.5.4.1-SNAPSHOT -Dpackaging=jar
```
然后再编译就成功了：
![image](https://user-images.githubusercontent.com/30398606/179916953-1104566b-03ab-41e5-a391-013d7173d183.png)



![image](https://user-images.githubusercontent.com/30398606/179916492-a047ae64-8097-4b41-893b-61deb30a5794.png)


Ref:
- [maven项目中，本地获取到jar文件，而远程仓库没有该jar文件，如何把jar文件打到本地仓库](https://blog.51cto.com/u_15060547/3790460)
- [IDEA MAVEN工程拉取本地jar包](https://icode.best/i/34891747617088)
