### 子域名
- https://github.com/aboul3la/Sublist3r

- 通过Censys.io 查看子域名的证书：
443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names:snapchat.com

- certspotter的API获取子域名：
https://sslmate.com/certspotter/

- Crt.sh

根据一些子域名进行http(s)请求，看哪些是在线的：
https://github.com/tomnomnom/httprobe


- shodan.io
- Ports: 8443, 8080, 8180, etc
- Title: “Dashboard [Jenkins]”
- Product:Tomcat
- Hostname: somecorp.com
- Org: evilcorp
- ssl: Google




### 工具
自动化信息搜集工具（只需要给一个域名）
https://github.com/nahamsec/LazyRecon
自动根据js找出里面的AJAX请求，寻找隐藏的API
https://github.com/nahamsec/JSParser

### WEB截屏
用于
webscreenshot.py

### Google Dork
site.com +inurl:dev -cdn 

### 参考
- https://www.youtube.com/watch?v=amihlWTtkMA
- https://docs.google.com/presentation/d/1xgvEScGZ_ukNY0rmfKz1JN0sn-CgZY_rTp2B_SZvijk/edit#slide=id.g455c1d71d4_0_0



### 实例
#### steam wallet支付漏洞
- https://hackerone.com/reports/1295844
- https://www.youtube.com/watch?v=4D-6nWIRZLU

原理：利用字符串被拼接后进行hash的方式，拼接不同的key/value对，拼接出相同的hash值，从而实现任意数额支付。
