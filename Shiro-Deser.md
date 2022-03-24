### 环境搭建
```bash
git clone https://github.com/apache/shiro.git
# wget https://codeload.github.com/apache/shiro/zip/shiro-root-1.2.4
git checkout shiro-root-1.2.4  
cd ./shiro/samples/web  
mvn package -D maven.skip.test=true
```
前提需要在$MVAEN_HOME以及~/.m2/目录下新建`toolchains.xml`问价：
```xml
<toolchain>
  <type>jdk</type>
  <provides>
    <version>1.6</version>
    <vendor>sun</vendor>
  </provides>
  <configuration>
    <jdkHome>D:\repos\Java\jdk1.6.0_45</jdkHome>
  </configuration>
</toolchain>
```
开始只在~/.m2/目录下新建发现不行，后来在$MVAEN_HOME目录下增加了几行代码就可以了。

Shiro反序列化的要点：

- rememberMe cookie
- CookieRememberMeManager.java
- Base64
- AES
- 加密密钥硬编码
- Java serialization

github搜索关键词

```java
- securityManager.rememberMeManager.cipherKey
- cookieRememberMeManager.setCipherKey
- setCipherKey(Base64.decode
```


配置文件路径或者名
```
- WEB-INF/shiro.ini
- ShiroConfig.java
```
### 参考
- https://paper.seebug.org/shiro-rememberme-1-2-4/
- http://www.lmxspace.com/2019/10/17/Shiro-%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E8%AE%B0%E5%BD%95/
