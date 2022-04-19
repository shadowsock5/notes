```
对于 Amazon Linux 2 或 Amazon Linux AMI，用户名称是 ec2-user。

对于 CentOS AMI，用户名称是 centos。

对于 Debian AMI，用户名称是 admin 或 root。

对于 Fedora AMI，用户名为 ec2-user 或 fedora。

对于 RHEL AMI，用户名称是 ec2-user 或 root。

对于 SUSE AMI，用户名称是 ec2-user 或 root。

对于 Ubuntu AMI，用户名称是 ubuntu。
```
https://www.cnblogs.com/yelao/p/12589098.html


登录：
```
Last login: Tue Apr 19 02:50:45 2022 from ec2-xxxxxxxx.us-west-1.compute.amazonaws.com

       __|  __|_  )
       _|  (     /   Amazon Linux 2 AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-2/
[ec2-user@ip-xxxxx ~]$ id
uid=1000(ec2-user) gid=1000(ec2-user) groups=1000(ec2-user),4(adm),10(wheel),190(systemd-journal)
[ec2-user@ip-xxxxx ~]$ cat /etc/issue
\S
Kernel \r on an \m


```


![image](https://user-images.githubusercontent.com/30398606/163912942-61a2c939-9e49-4733-b678-eaf43ab37a2f.png)

```
/usr/local/gradle
/usr/lib/jvm/java
/usr/local/apache-maven/bin
/usr/local/apache-maven
```

默认的ec2用户主机上的端口是这样的：
```
[ec2-user@ip-172-31-6-246 ~]$ sudo netstat -plnt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      2613/rpcbind
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      3265/sshd
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      3028/master
tcp6       0      0 :::111                  :::*                    LISTEN      2613/rpcbind
tcp6       0      0 :::22                   :::*                    LISTEN      3265/sshd
```
而Elastic Beanstalk应用服务器上的端口是：
```
PORT     STATE SERVICE
21/tcp   open  ftp
53/tcp   open  domain
80/tcp   open  http
443/tcp  open  https
554/tcp  open  rtsp
1723/tcp open  pptp
8080/tcp open  http-proxy
8443/tcp open  https-alt
```

详细列表：
```
21/tcp   open  ftp-proxy   Zscaler ftp proxy 6.1
53/tcp   open  domain      (unknown banner: Secured !!! Here no any useful information to you !!!)
| fingerprint-strings:
|   DNSVersionBindReqTCP:
|     version
|     bind
|_    65Secured !!! Here no any useful information to you !!!
| dns-nsid:
|_  bind.version: Secured !!! Here no any useful information to you !!!
80/tcp   open  http        nginx 1.18.0
|_http-title: 502 Bad Gateway
|_http-server-header: nginx/1.18.0
443/tcp  open  https?
554/tcp  open  rtsp?
1723/tcp open  pptp?
|_pptp-version: ERROR: Script execution failed (use -d to debug)
8080/tcp open  http-proxy?
8443/tcp open  https-alt?
```

碰到502：
Ref:
- https://aws.amazon.com/premiumsupport/knowledge-center/load-balancer-http-502-errors/
