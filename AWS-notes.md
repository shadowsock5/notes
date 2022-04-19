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
