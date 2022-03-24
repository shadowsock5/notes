参考：
- [SPF 记录：原理、语法及配置方法简介](http://www.renfei.org/blog/introduction-to-spf.html)
- [钓鱼邮件的投递和伪造](https://xz.aliyun.com/t/6325)


### 什么是SPF
Sender Policy Framework 的缩写，一种以IP地址认证电子邮件发件人身份的技术。

### 邮件为什么可以被伪造
邮件为什么可以被伪造呢，最根本的原因就是SMTP协议不会验证发送者的身份。


### SPF原理
SPF 记录实际上是服务器的一个 DNS 记录（只有拥有这个域名的人才有权限修改）。

由于SMTP协议并不会验证发件人的身份，比如发件人可以声称自己是whatever@gmail.com，然后发送邮件的邮件服务器的IP（通过网络层获得）是173.194.72.103。
如果没有SPF，则接收方的SMTP服务器就相信了这个邮件的发件人是whatever@gmail.com。
如果有SPF，为了确认发件人确实来自whatever@gmail.com，则接收方邮件服务器会去查gmail.com的SPF记录。
如果gmail.com是SPF设置了允许173.194.72.103的主机发送邮件，则认为合法，否则认为不合法，设置为垃圾邮件（SPAM）。



