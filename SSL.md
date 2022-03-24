## SSL握手过程

单向SSL握手（one-way）和双向SSL握手（Mutual SSL）
通常在我们浏览HTTPs网站的时候，只进行了单向SSL握手，因为只需要Client验证Server的有效性。而双向SSL出现了双方都需要验证对方身份的情况。

### 1. Client Hello (Client → Server)
客户端发送一些信息给服务端，以作为服务端后续开启HTTPs连接使用。
- SSL/TLS版本号
比如，TLS 1.2 的client_version 为3,3  因为TLS 1.0被视为Secure Sockets Layer（SSL 3.0）的最低分支， TLS 1.0 is 3,1, TLS 1.1 is 3,2。依次类推。
- 32字节的random byte string（用于后续密钥的计算），其中前四个字节代表当前的日期和时间，其余28字节是随机数生成器产生的。
- Session ID
用来标识此次会话。若session_id为空，则Server会开启一个新的Session；若session_id 不为空，则Server会从之前缓存的sessions中搜索，若找到了则会继续那个session。
- compression_methods（存在风险，不建议使用）
压缩方式，用于压缩SSL数据包。压缩可以降低带宽开销以及增加传输速率。
- Cipher Suites（加密套件）
加密算法的集合。一般情况，每个加密套件包含一个加密算法，用于处理以下任务：密钥交换、认证（authentication）、大量数据(bulk)交换、消息认证。Client将加密套件以list的形式发送
- Extensions

```
*** ClientHello, TLSv1.2
RandomCookie: *** ClientHello, TLSv1.2
RandomCookie: GMT: -1892413556 bytes = { GMT: -351008774 bytes = { 169, 131, 204, 213, 154, 96, 7, 136, 43, 142, 232, 138, 148, 171, 52, 226, 155, 202, 145, 57, 210, 132, 227, 182, 67, 222, 161, 28, 20 }
Session ID: 239, 10, 92, 143, 185, {}
93, Cipher Suites: [Unknown 0x8a:0x8a, TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, Unknown 0xcc:0xa9, Unknown 0xcc:0xa8, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_AES_128_GCM_SHA256, TLS_RSA_WITH_AES_256_GCM_SHA384, TLS_RSA_WITH_AES_128_CBC_SHA, TLS_RSA_WITH_AES_256_CBC_SHA, SSL_RSA_WITH_3DES_EDE_CBC_SHA]
………………………………………………
```
其中`TLS v1.2`表示客户端只支持TLS v1.2及以下TLS版本。
#### Client Hello Demo
![image.png](https://xzfile.aliyuncs.com/media/upload/picture/20190430153318-38fa0e62-6b1a-1.png)

### 2. Server Hello (Server → Client)
- 服务端发送从客户端收到的CipherSuite 列表中选出来的CipherSuite ，然后服务端还发送自身的证书；
- 另一个random byte string
- 如果服务端有验证客户端证书的需求，它会发送`client certificate request`消息给客户端
```
*** ServerHello, TLSv1.2
RandomCookie: GMT: 1518335451 bytes = { 19, 150, 56, 42, 168, 202, 151, 43, 174, 226, 187, 53, 135, 67, 244, 170, 59, 176, 105, 150, 50, 112, 167, 83, 192, 48, 171, 64 }
Session ID: {91, 128, 246, 219, 26, 93, 46, 172, 85, 212, 221, 79, 20, 186, 108, 134, 200, 239, 150, 102, 172, 24, 125, 171, 137, 53, 5, 130, 53, 228, 2, 195}
Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
Compression Method: 0
Extension renegotiation_info, renegotiated_connection: <empty>
***
```
#### Server Hello Demo
![image.png](https://xzfile.aliyuncs.com/media/upload/picture/20190430153206-0e669a94-6b1a-1.png)

### 3. Server Certificate (Server → Client)
Server发送一个由其private key签名的TLS/SSL证书，带上它的public key，用于Client验证。
Client验证Server的证书，细节参考：https://www.ibm.com/support/knowledgecenter/SSFKSJ_7.1.0/com.ibm.mq.doc/sy10670_.htm
![image.png](https://xzfile.aliyuncs.com/media/upload/picture/20190430154330-a5da5e5a-6b1b-1.png)

### 4. Client Certificate (Client → Server, 可选)
在少数情况下，Server需要对Client的身份进行认证。
Client使用Server's 公钥加密生成一个random byte string，然后将其发送给Server（之后将用于对密钥进行计算，加密后续传输的数据）。然后，Server验证Client的证书，详情参考：https://www.ibm.com/support/knowledgecenter/SSFKSJ_7.1.0/com.ibm.mq.doc/sy10670_.htm

### 5. Server Key Exchange (Server → Client)
仅当Server提供的证书不足以使Client完成pre-master secret交换时，才发送此消息。
若Server发送了`client certificate request`消息，Client收到后，会使用Client's私钥加密生成一个random byte string，连同Client's证书发送给Server。或者发送`no digital certificate alert`，这个alert只是一个警告，在某些协议的实现中，如果Client的认证是必需的，这样会导致握手失败。

![image.png](https://xzfile.aliyuncs.com/media/upload/picture/20190430154602-00b3645c-6b1c-1.png)

### 6. Server Hello Done (Server → Client)
Server发送这个表示：Server Hello消息已经结束。

### 7. Client Key Exchange (Client → Server)
Client从Server接受到Server Hello Done消息之后，就会发送Client Key Exchange消息。在Client验证完成Server的证书之后，就会准备创建pre-master。 key。
#### Pre-Master Secret
在Client发送pre-master key之前，Client会使用从Server发来的证书中提取出来的Server public key来加密。这也意味着只有这个Server可以解密消息。这就是握手中的非对称加密的体现了。
![image.png](https://xzfile.aliyuncs.com/media/upload/picture/20190430154739-3a5c542a-6b1c-1.png)

#### Master Secret
在Server收到pre-master key之后，它会用其private key解密。然后就使用伪随机函数（pseudorandom function (PRF)），基于之前交换的Client Random和Server Random来计算master secret key。
```
master_secret = PRF(pre_master_secret, "master secret", ClientHello.random + ServerHello.random) [0..47];
```
然后，这个48个字节大小的master secret key就会被Client和Server用来对称加密之后通信的数据。

### 8. Client Change Cipher Spec (Client → Server)
到这里，Client就已经准备好切换到安全的加密环境了。`Change Cipher Spec`协议就是用来变更加密方式的。从现在开始，任意从Client发出的数据将会使用shared key来加密了。
实际抓包过程发现，这一步已经在第7步（Client Key Exchange (Client → Server)）中有了：
![image.png](https://xzfile.aliyuncs.com/media/upload/picture/20190430160033-07e1d040-6b1e-1.png)
只剩下这个：
![image.png](https://xzfile.aliyuncs.com/media/upload/picture/20190430160230-4dc2b4ee-6b1e-1.png)

### 9. Client Handshake Finished (Client → Server)
在接下来的SSL/TLS会话中，Server和Client就可以通过使用共享密钥（shared secret key）对称加密的方式进行通信了。
下面就是Client发送的一个被SSL加密的HTTP请求：
![image.png](https://xzfile.aliyuncs.com/media/upload/picture/20190430160404-858d82c8-6b1e-1.png)
Server返回的内容比较多，所以分成几个包来发送。
![image.png](https://xzfile.aliyuncs.com/media/upload/picture/20190430160753-0e4b4ad2-6b1f-1.png)

### 完整的SSL握手过程
来自IBM：![](https://www.ibm.com/support/knowledgecenter/SSFKSJ_7.1.0/com.ibm.mq.doc/sy10660a.gif)
来自AWVS：![](https://www.acunetix.com/wp-content/uploads/2017/01/image34.png)

### 参考
https://medium.com/@kasunpdh/ssl-handshake-explained-4dabb87cdce
https://www.ibm.com/support/knowledgecenter/en/SSFKSJ_7.1.0/com.ibm.mq.doc/sy10660_.htm
https://www.acunetix.com/blog/articles/establishing-tls-ssl-connection-part-5/
