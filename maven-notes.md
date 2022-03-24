## 依赖检查
1、命令行使用:
```
mvn dependency:tree -Dincludes=com.alibaba:fastjson
```

2、IDEA插件：
Maven Helper
- [使用Maven Helper解决Maven插件冲突](https://segmentfault.com/a/1190000017542396)



## 附录

> Every Maven project has a packaging type. If it is not specified in the POM, then the default value "jar" would be used.


Ref:
- https://maven.apache.org/guides/introduction/introduction-to-the-pom.html
- https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html
- https://maven.apache.org/guides/introduction/introduction-to-optional-and-excludes-dependencies.html



### mavan中的artifact版本问题
Ref:
- https://coderanch.com/t/625784/build-tools/version-downloaded-Maven-version-defined
- 

在项目根目录中发现`org.springframework.security:spring-security-saml2-service-provider`的版本是5.5.1，
```
mvn dependency:tree -Dincludes=org.springframework.security:spring-security-saml2-service-provider

[INFO] --- maven-dependency-plugin:3.1.2:tree (default-cli) @ xxxxx-client ---
[INFO] cn.com.yyyyyyy:xxxxx-client:jar:0.0.1-SNAPSHOT
[INFO] \- org.springframework.security:spring-security-saml2-service-provider:jar:5.5.1.RELEASE:compile


[INFO] --- maven-dependency-plugin:3.1.2:tree (default-cli) @ xxxxx-core ---
[INFO] cn.com.yyyyyyy:xxxxx-core:jar:0.0.1-SNAPSHOT
[INFO] \- cn.com.yyyyyyy:xxxxx-client:jar:0.0.1-SNAPSHOT:compile
[INFO]    \- org.springframework.security:spring-security-saml2-service-provider:jar:5.5.1:compile
```
知道最终是在xxxxx-client中引入的，于是在xxxxx-client子模块中，找到pom，
发现其内容是：
```xml
        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-saml2-service-provider</artifactId>
        </dependency>
```
并没有直接指定版本，于是自己尝试手动将其设置为: 5.3.0.RELEASE
但是重新编译之后，调试起来发现项目依然使用的是5.5.1，

使用


在xxxxx-client模块下使用命令：
```bash
mvn -P pom.xml help:effective-pom -Dverbose -Doutput=result2.xml
```
结果是：
```
<dependencyManagement>
...
      <dependency>
        <groupId>org.springframework.security</groupId>  <!-- org.springframework.security:spring-security-bom:5.5.1, line 127 -->
        <artifactId>spring-security-saml2-service-provider</artifactId>  <!-- org.springframework.security:spring-security-bom:5.5.1, line 128 -->
        <version>5.5.1</version>  <!-- org.springframework.security:spring-security-bom:5.5.1, line 129 -->
      </dependency>
...
</dependencyManagement>

<dependencies>
...
    <dependency>
      <groupId>org.springframework.security</groupId>  <!-- cn.com.yyyyyyy:agent-client:0.0.1-SNAPSHOT, line 30 -->
      <artifactId>spring-security-saml2-service-provider</artifactId>  <!-- cn.com.yyyyyyy:agent-client:0.0.1-SNAPSHOT, line 31 -->
      <version>5.3.0.RELEASE</version>  <!-- cn.com.yyyyyyy:agent-client:0.0.1-SNAPSHOT, line 32 -->
      <scope>compile</scope>
    </dependency>
...
</dependencies>
```
发现我手动指定的版本号只是在`compile`这个scope。后来搜索找到这个[which version will be downloaded by Maven if version is not defined in dependency](https://coderanch.com/t/625784/build-tools/version-downloaded-Maven-version-defined)，才知道可能需要去parent里去找。于是找到
![image](https://user-images.githubusercontent.com/30398606/146705636-c4d1d540-7be4-42b5-9234-c2c2fc189da4.png)



最后在~\.m2\repository\org\springframework\security\spring-security-bom\5.5.1\spring-security-bom-5.5.1.pom
找到了
```xml
 <dependencyManagement>
   <dependencies>
         <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-saml2-service-provider</artifactId>
        <version>5.5.1</version>
      </dependency>
    </dependencies>   
</dependencyManagement>
````


如何排除parent中引入的依赖版本，指定自己希望的版本？
Ref:
- https://stackoverflow.com/questions/2681759/is-there-anyway-to-exclude-artifacts-inherited-from-a-parent-pom
- 
```xml
    <dependencyManagement>
        <dependencies>
          ...
            <dependency>
                <groupId>org.springframework.security</groupId>
                <artifactId>spring-security-saml2-service-provider</artifactId>
                <version>5.3.0.RELEASE</version>
            </dependency>
          ...
        </dependencies>
    </dependencyManagement>
```
然后刷新一下maven，
![image](https://user-images.githubusercontent.com/30398606/146706675-87aa7e1f-f919-4f85-85bb-d5a782b66390.png)
完成。
