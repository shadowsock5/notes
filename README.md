# notes

## Bug Bounties
除了hackerone和bugcrowd之外：

- https://www.openbugbounty.org/  这个可以作为搜集一些常见被报告的网站信息
- https://yeswehack.com/programs  只有少数有bug bounty

## 信息收集
企业的分公司，全资子公司，网站域名、手机app,微信小程序，企业专利品牌信息，企业邮箱，电话。
参考：
- [SRC混子的漏洞挖掘之道](https://xz.aliyun.com/t/8501)
- [浅谈攻防演练中的信息收集](https://xz.aliyun.com/t/8578)

### 资产管理
- https://github.com/CTF-MissFeng/bayonet
- https://github.com/CTF-MissFeng/Watchdog

### 基本信息
企查查、天眼查淘宝都有那种一天的会员。对于我们信息收集其实已经够用。

- [天眼查](https://www.tianyancha.com/)
- [企查查](https://www.qcc.com/)
- https://www.whois.com/whois/
- http://whois.chinaz.com/
- https://whois.aliyun.com/
- https://www.whois365.com/cn/
- https://www.aizhan.com/
- http://www.miitbeian.gov.cn/publish/query/indexFirst.action

### IP地址段收集
- https://bgp.he.net/

比如收集百度：
https://bgp.he.net/search?search%5Bsearch%5D=baidu&commit=Search

- https://github.com/j3ssie/metabigor/releases
这个工具用到的API是:(http://asnlookup.com/api/lookup?org=baidu, https://bgp.he.net/search?search%5Bsearch%5D=baidu&commit=Search)

- https://github.com/yassineaboukir/Asnlookup
这个工具其实也是用的http://asnlookup.com/api/lookup?org=baidu

然后用ASN枚举工具，枚举出某个ASN号码的IP段：
- https://github.com/caffix/amass/releases

Google搜集C段：
- site:202.202.43.*

### IP归属查询
- https://img.cy/ip
- http://www.ip138.com/ips1388.asp
- http://ip.soshoulu.com/
- https://www.ipip.net/ip.html

### 绕过CDN查找真实IP
- https://github.com/Tai7sy/fuckcdn
- https://github.com/superfish9/hackcdn


### 绕WAF
- https://github.com/Bo0oM/WAF-bypass-Cheat-Sheet

### 子域名

- https://github.com/shmilylty/OneForAll
注意升级！使用代理和不使用代理都来一套。

### js信息收集
- https://github.com/p1g3/JSINFO-SCAN
- https://github.com/Threezh1/JSFinder

### 指纹识别

#### 1、Ehole
下载地址：
https://github.com/EdgeSecurityTeam/EHole
使用方法：
```
./Ehole-darwin -l url.txt   //URL地址需带上协议,每行一个
./Ehole-darwin -f 192.168.1.1/24  //支持单IP或IP段,fofa识别需要配置fofa密钥和邮箱
./Ehole-darwin -l url.txt -json export.json  //结果输出至export.json文件
```

#### 2、Glass
下载地址：
https://github.com/s7ckTeam/Glass
使用方法：
```
python3 Glass.py -u http://www.examples.com  // 单url测试
python3 Glass.py -w domain.txt -o txt/html  // url文件内
```

#### 3. bscan

https://github.com/broken5/bscan

#### 4. dismap
https://github.com/zhzyker/dismap

参考：
- [SRC信息收集思路分享](https://xz.aliyun.com/t/10418)

### Window提权补丁
- https://bugs.hacking8.com/tiquan/

### app抓包
- [如何利用http tunnel使用burpsuite拦截某个app的tcp数据包（非http）做安全分析](https://xz.aliyun.com/t/8640)

### github用户邮箱收集
https://github.com/paulirish/github-email/

### DNS反查
- http://dns.chacha.cn/
- https://github.com/mandatoryprogrammer/cloudflare_enum
- http://ptrarchive.com/

### 在线端口扫描
- https://hackertarget.com/tcp-port-scan/

#### Demo
```
curl "https://api.hackertarget.com/nmap/?q=baidu.com"
```

### 编码/进制/加密转换
- [Hex to ASCII](https://www.rapidtables.com/convert/number/hex-to-ascii.html)
- [字符串在线对比](https://text-compare.com/)
- [各种文件在线diff](https://www.diffnow.com/)
- [在线进制转换](http://tool.oschina.net/hexconvert)
- http://www.ximizi.com/JinZhi_ZhuanHuan.php
- [二维码](http://jiema.wwei.cn/)

### Hash识别/破解
- [hash识别](https://www.onlinehashcrack.com/hash-identification.php)
- http://www.fileformat.info/tool/hash.htm
- http://www.cmd5.com/
- https://crackstation.net/
- https://passwordrecovery.io/sha256/
- https://www.nirsoft.net/utils/hashmyfiles-x64.zip

### 社工字典生成器
- https://github.com/HongLuDianXue/BaiLu-SED-Tool
- https://github.com/huyuanzhi2/password_brute_dictionary

### GitHub的dorks
- https://github.com/obheda12/GitDorker/tree/master/Dorks

### pcap文件在线分析
- https://packettotal.com/

### DNSLog
- http://ceye.io/
- http://dnsbin.zhack.ca/
- http://dnslog.cn/
- xxx.burpcollaborator.net

### 短网址
- http://sina-t.cn/

### 短信接收平台
- https://www.becmd.com/
- http://z-sms.com/lv?pho_num=17061084088&1
- https://www.materialtools.com/
- https://yunduanxin.net/China-Phone-Number/

### 文件/文本共享
- https://github.com/dutchcoders/transfer.sh
- https://mega.nz/
- https://pastebin.com/

### malware在线分析/下载
- https://www.hybrid-analysis.com/
- https://www.virustotal.com/
- http://malc0de.com/database/
- https://malwr.com/analysis/search/
- https://x.threatbook.cn/
- https://koodous.com/

### 图像识别
- https://zhcn.109876543210.com/
- https://onlineocr.net/

### 证件照处理
- https://www.tooleyes.com/app/id_photo.html
- https://www.gaitubao.com/bgcolor
- https://www.bgconverter.com/


### 技术文章
- https://xz.aliyun.com/
- https://www.anquanke.com/
- https://www.freebuf.com/
- http://paper.seebug.org
- https://bbs.ichunqiu.com
- https://bbs.pediy.com/
- https://www.52pojie.cn

### jdk download
- https://archive.org/details/jdk-7u80-windows-x64_201809
- https://files-cdn.liferay.com/mirrors/download.oracle.com/otn-pub/java/jdk/7u80-b15/

#### Demo
```
"burp" site:https://xz.aliyun.com/ OR https://www.anquanke.com/ OR http://paper.seebug.org OR https://www.freebuf.com/ OR https://bbs.ichunqiu.com OR https://bbs.pediy.com/ OR https://www.52pojie.cn
```

### 短网址
- http://sina-t.cn/

### 最新漏洞&&技术文章
- [feedly RSS](feedly-6f97a3f2-4440-4635-8994-74cb0baef02b-2020-09-22.opml)

### Gif录制工具（Mac & Windows）
- https://www.cockos.com/licecap/
