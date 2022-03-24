# Mybatis框架下的SQL注入漏洞

## 常见基于MyBatis的业务代码
指定配置文件`mybatis-config.xml`（这个配置文件会引用其他的相关的配置），载入需要的信息（驱动url、用户名密码、sql配置等）
```java
public class MybatisDemo {

    private SqlSessionFactory sqlSessionFactory;

    @Test
    public void testAutoMapping() throws IOException {
        //-------------第一阶段-------------------
        // 创建SqlSessionFactory
        String resource = "mybatis-config.xml";
        InputStream inputStream = Resources.getResourceAsStream(resource);
        sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
        inputStream.close();

        //-------------第二阶段-------------------
        //获取 SqlSession
        SqlSession sqlSession = sqlSessionFactory.openSession();
        //获取对应 Mapper
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);


        //-------------第三阶段-------------------
        // 使用Mapper执行查询语句并返回单条数据
        User user = mapper.selectByPrimaryKey(121312312312L);
        System.out.println(user);

        // 使用Mapper执行查询语句并返回多条数据
        List<User> users = mapper.selectAll();

    }
}
```

### 实体类：entity/User.java
某个JavaBean。

### 映射器：mapper/UserMapper.java
只是一个接口，主要看方法名，返回类型，接收参数。
```java
public interface UserMapper {

    User selectByPrimaryKey(long userId);

    List<User> selectAll();
}
```
与`UserMapper.xml`的对应关系：
方法名对应`id`，返回类型对应`resultType`。

### 配置文件（resources目录下）：mybatis-config.xml
```xml
<configuration>
    <properties resource="db.properties"/>

    <settings>
        <setting name="mapUnderscoreToCamelCase" value ="true"/>
        <setting name="aggressiveLazyLoading" value="false"/>
    </settings>

    <typeAliases>
        <package name="com.paul.mybatis.entity" />
    </typeAliases>

    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="UNPOOLED">
                <property name="driver" value="${jdbc_driver}"/>
                <property name="url" value="${jdbc_url}"/>
                <property name="username" value="${jdbc_username}"/>
                <property name="password" value="${jdbc_password}"/>
            </dataSource>
        </environment>
    </environments>

    <mappers>
        <mapper resource="sqlmapper/UserMapper.xml"/>

    </mappers>

</configuration>
```
上面的配置引入了另外两个配置文件：
#### db.properties
就是jdbc的url、用户名、密码
```
jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/mybatis?useUnicode=true&characterEncoding=utf8
jdbc.username=root
jdbc.password=root
```

#### sqlmapper/UserMapper.xml
实现Mapper接口中的方法，`id`对应方法名，`resultType`对应返回值类型。`select`标签内的是sql语句。
```xml
<mapper namespace="com.paul.mybatis.mapper.UserMapper">

    <select id="selectByPrimaryKey" resultType="com.paul.mybatis.entity.User">
        select *
        from t_user
        where userId = #{userId}
    </select>

    <select id="selectAll" resultType="com.paul.mybatis.entity.User">
        select *
        from t_user
    </select>

</mapper>
```

#### Annotation实现Mapper接口
除了使用xml实现Mapper，还可以用注解（Annotation）方式来实现。
```java
@Mapper
public interface UserMapper {
    @Select("SELECT * FROM user WHERE id= #{id}")
    User getById(@Param("id") int id);
}
```


## 场景分析
### 1. 模糊查询like：
```
<select id="selectStudentByFuzzyQuery" resultMap="studentMap">
    SELECT *
    FROM student
    WHERE student.stu_name
            LIKE '%#{stuName}%'
</select>
```
MyBatis会把`%#{stuName}%`作为要查询的参数，数据库会执行
```
SELECT * FROM student WHERE student.stu_name LIKE '%#{stuName}%'
```
导致查询失败。
于是为了避免报错，研发人员将SQL查询语句改成`${}`，但是这样又存在SQL注入的风险。
### 2. 多值查询in之后的参数
```
Select * from news where id in (#{id})，
```
这样的SQL语句虽然能执行但得不到预期结果，于是研发人员将SQL查询语句修改如下：
```
Select * from news where id in (${id})，
```

### 3. order by之后
```
Select * from news where title ='京东' order by #{time} asc，
```
但由于发布时间time不是用户输入的参数，无法使用预编译。研发人员将SQL查询语句修改如下：
```
Select * from news where title =‘京东’ order by ${time} asc，
```
修改之后，程序通过预编译，但是产生了SQL语句拼接问题，极有可能引发SQL注入漏洞。

由于order by语句要求传入字段名或者字段位置：
```sql
select username from users ORDER BY id
select username from users ORDER BY 1
```
如果传入的是引号包裹的字符串，那么 ORDER BY 会失效，如：
```sql
SELECT * FROM user ORDER BY 'id'
```
所以，如果要动态传入 ORDER BY 参数，只能用字符串拼接的方式，如：

```java
String sql = "SELECT * FROM user ORDER BY " + column;
```
那么这样依然可能会存在SQL注入的问题。

## 修复建议
### 1. 模糊查询like SQL注入修复建议
使用数据库自带的 CONCAT ，将 % 和我们用 #{} 传入参数连接起来，这样就既不存在注入的问题，也能满足需求啦。
```xml
<select id="getUserListLikeConcat" resultType="org.example.User">
	SELECT * FROM user WHERE name LIKE concat ('%', #{name}, '%')
</select>
```
或者
```xml
<select id="getUserListLike" resultType="org.example.User">
    <bind name="pattern" value="'%' + name + '%'" />
    SELECT * FROM user 
    WHERE name LIKE #{pattern}
</select>
```
采用预编译机制，避免了SQL语句拼接的问题，从根源上防止了SQL注入漏洞的产生。

### 2. in之后的参数SQL注入修复建议
可使用Mybatis自带循环指令（`foreach`）解决SQL语句动态拼接的问题：
```
<select id="selectUserIn" resultType="com.example.User">
  SELECT * FROM user WHERE name in
  <foreach item="name" collection="nameList" 
           open="(" separator="," close=")">
        #{name}
  </foreach>
</select>
```

### 3. order by(GROUP BY) SQL注入修复建议--在Java层面做映射
两种情况：
#### 1、column是字符型
手动过滤，列举出字段名，进行条件判断：
```java
String column = "id";
String sql ="";
switch(column){
    case "id":
        sql = "SELECT * FROM user ORDER BY id";
        break;
    case "username":
        sql = "SELECT * FROM user ORDER BY username";
        break;
    ......
}
```

#### column 是 int 型
因为 Java 是强类型语言，当用户传递的参数与后台定义的参数类型不匹配，程序会抛出异常，赋值失败。所以，不会存在注入的问题。

## 注
mybatis框架中`#{变量}`对应JDBC中的预编译机制(`java.sql.PreparedStatement`)，不存在SQL注入漏洞；
`${变量}`对应SQL语句拼接方式(`java.sql.Statement`)，存在SQL注入风险。



## 漏洞分类挖掘技巧
根据挖掘经验，白盒挖掘层面大致可以将SQLi的类型分为六类：

- 1、入参直接动态拼接(未使用预编译语句)；

- 2、预编译动态拼接（使用预编译语句）；

- 3、框架注入（Mybatis、Hibernate）；
Hibernate:
Mybatis: 挖掘技巧则是在注解中或者Mybatis相关的配置文件中搜索 `$`
- 4、order by、like、in等语句不能预编译导致的注入；

- 5、%和_绕过预编译；

- 6、SQLi检测绕过

### 快速定位xml中的可能sqli
```bash
grep -rn '\$' `find .|grep Mapper.xml`
```

## 参考
- [Mybatis框架下SQL注入漏洞面面观](https://mp.weixin.qq.com/s/TXXJAOlaLEHngNjx1cv0Sw)
- [给自己一个更安全的 mysql](https://klionsec.github.io/2017/11/22/mysqlconfigsec/)
- [Java SQL 注入学习笔记](https://b1ngz.github.io/java-sql-injection-note/)
- [从1开始的Java代码审计·第三弹·SQL注入](https://jayl1n.github.io/2018/11/15/java-audit-step-by-step-3/)
- [java框架之MybatisSQL注入漏洞](https://zhuanlan.zhihu.com/p/28168319)
- [Java代码审计汇总系列(一)——SQL注入](https://cloud.tencent.com/developer/article/1534109)
- [本以为用的MyBatis框架就万无一失了，没想到还是被黑客注入了，我真的无语了！](https://mp.weixin.qq.com/s/yr5kp91m6dWrFDZT28Vohw)
- [自己实现一个 MyBatis 框架](https://www.cnblogs.com/paulwang92115/p/12130224.html)
- [SQLi in Java](https://www.kingkk.com/2019/11/SQLi-in-Java/)
- [Java SQL注入深入分析](https://xz.aliyun.com/t/10593)
