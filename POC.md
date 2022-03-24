### 命令执行兼容Windows和Linux
参考：
https://www.cdxy.me/?p=701

```bash
ping -n 3 127.0.0.1 || ping -c 3 127.0.0.1
```
结果：
Linux：

```bash
$ ping -n 3 127.0.0.1 || ping -c 3 127.0.0.1
connect: Invalid argument
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.019 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.030 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.084 ms

--- 127.0.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2026ms
rtt min/avg/max/mdev = 0.019/0.044/0.084/0.028 ms
```

Windows:
```bash
ping -n 3 127.0.0.1 || ping -c 3 127.0.0.1

正在 Ping 127.0.0.1 具有 32 字节的数据:
来自 127.0.0.1 的回复: 字节=32 时间<1ms TTL=128
来自 127.0.0.1 的回复: 字节=32 时间<1ms TTL=128
来自 127.0.0.1 的回复: 字节=32 时间<1ms TTL=128

127.0.0.1 的 Ping 统计信息:
    数据包: 已发送 = 3，已接收 = 3，丢失 = 0 (0% 丢失)，
往返行程的估计时间(以毫秒为单位):
    最短 = 0ms，最长 = 0ms，平均 = 0ms
```


还有一种方法，执行不存在的命令，返回`Cannot run program`，即可认为存在命令执行。
```java
java.io.IOException: CreateProcess error=2, 系统找不到指定的文件。
	at java.lang.ProcessImpl.create(Native Method)
	at java.lang.ProcessImpl.<init>(Unknown Source)
	at java.lang.ProcessImpl.start(Unknown Source)
Caused: java.io.IOException: Cannot run program "id": CreateProcess error=2, 系统找不到指定的文件。
	at java.lang.ProcessBuilder.start(Unknown Source)
	at java.lang.Runtime.exec(Unknown Source)
	at java.lang.Runtime.exec(Unknown Source)
	at java.lang.Runtime.exec(Unknown Source)
```
或者
```java
java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
Caused: java.io.IOException: Cannot run program "xxx": error=2, No such file or directory
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1048)
	at java.lang.Runtime.exec(Runtime.java:620)
	at java.lang.Runtime.exec(Runtime.java:450)
	at java.lang.Runtime.exec(Runtime.java:347)
```
