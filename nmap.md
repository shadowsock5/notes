## nmap扫描方式原理（与TCP协议/平台的网络API有关）
### SYN（nmap默认）
通常被称为半开放扫描（因为自己先SYN，然后收到服务端的SYN/ACK之后并不ACK，而是RST所以并不建立TCP连接）。
#### 原理
发送`SYN`包，
- 如果收到`SYN/ACK`=> 端口开放；
- 如果收到`RST`=> 端口关闭；
- 如果未收到回复=> 端口被屏蔽(Filtered)
由于仅发送SYB包，不建立完整TCP连接，相对隐蔽，效率高


### connect
建立完整的TCP连接（因为自己先SYN，然后收到服务端的SYN/ACK之后先ACK才RST，于是三次握手已完成，TCP连接建立）。
#### 原理
发起connect连接，
- 如果连接建立 => 端口开放
- 如果收到`RST` => 端口关闭 


### ACK
用于辅助SYN方式判断防火墙的情况。
#### 原理
发送ACK包，
- 如果收到RST包 => 没有被防火墙屏蔽
- 如果未收到RST包 => 被防火墙屏蔽


### FIN
只能用于探测是否被防火墙屏蔽
#### 原理
发送FIN，
- 如果收到RST => 端口关闭
- 如果未收到RST => 端口开放/屏蔽(`open|filtered`)

## 参考
- https://mp.weixin.qq.com/s/kX8KilrUobOtr7AJqaU7gg
