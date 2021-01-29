## SSRF发现&利用


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
