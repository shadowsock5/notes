检测方式：
> 使用如下脚本扫描也可以，直接连接目标服务发送JDWP-Handshake，然后接受到相同内容则说明是JDWP服务：
```py
import socket

client = socket.socket()
client.connect(("127.0.0.1", 8000))
client.send(b"JDWP-Handshake")

if client.recv(1024) == b"JDWP-Handshake":
 print("[*]JDWP Service!")

client.close()
```
参考：
- https://www.mi1k7ea.com/2021/08/06/%E6%B5%85%E6%9E%90JDWP%E8%BF%9C%E7%A8%8B%E4%BB%A3%E7%A0%81%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E/
