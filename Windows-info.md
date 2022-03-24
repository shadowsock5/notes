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
Systeminfo
```

或者
```
wmic qfe get Caption,Description,HotFixID,InstalledOn
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


### ICMP探测内网
```
for /L %I in (1,1,254) DO @ping -w 1 -n 1 192.168.85.%I | findstr "TTL="
```
