```cmd
java -javaagent:C:\repos\jSSLKeyLog-1.3\jSSLKeyLog.jar==C:\repos\jSSLKeyLog-1.3\keylog.txt -jar ./test.jar
Verbose SSL logging activated
Logging all SSL session keys to: C:\repos\jSSLKeyLog-1.3\keylog.txt
...
```
然后在wireshark里导入。

## Ref
- https://jsslkeylog.github.io/
- https://github.com/jsslkeylog/jsslkeylog/releases
- https://community.microfocus.com/collaboration/zenworks/w/zenworkstips/24540/decrypting-ssl-traffic-on-wireshark-using-jsslkeylog
