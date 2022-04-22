```
对于 Amazon Linux 2 或 Amazon Linux AMI，用户名称是 ec2-user。

对于 CentOS AMI，用户名称是 centos。

对于 Debian AMI，用户名称是 admin 或 root。

对于 Fedora AMI，用户名为 ec2-user 或 fedora。

对于 RHEL AMI，用户名称是 ec2-user 或 root。

对于 SUSE AMI，用户名称是 ec2-user 或 root。

对于 Ubuntu AMI，用户名称是 ubuntu。
```
https://www.cnblogs.com/yelao/p/12589098.html


登录：
```
Last login: Tue Apr 19 02:50:45 2022 from ec2-xxxxxxxx.us-west-1.compute.amazonaws.com

       __|  __|_  )
       _|  (     /   Amazon Linux 2 AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-2/
[ec2-user@ip-xxxxx ~]$ id
uid=1000(ec2-user) gid=1000(ec2-user) groups=1000(ec2-user),4(adm),10(wheel),190(systemd-journal)
[ec2-user@ip-xxxxx ~]$ cat /etc/issue
\S
Kernel \r on an \m


```


![image](https://user-images.githubusercontent.com/30398606/163912942-61a2c939-9e49-4733-b678-eaf43ab37a2f.png)

```
/usr/local/gradle
/usr/lib/jvm/java
/usr/local/apache-maven/bin
/usr/local/apache-maven
```

默认的ec2用户主机上的端口是这样的：
```
[ec2-user@ip-172-31-6-246 ~]$ sudo netstat -plnt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      2613/rpcbind
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      3265/sshd
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      3028/master
tcp6       0      0 :::111                  :::*                    LISTEN      2613/rpcbind
tcp6       0      0 :::22                   :::*                    LISTEN      3265/sshd
```
而Elastic Beanstalk应用服务器上的端口是：
```
PORT     STATE SERVICE
21/tcp   open  ftp
53/tcp   open  domain
80/tcp   open  http
443/tcp  open  https
554/tcp  open  rtsp
1723/tcp open  pptp
8080/tcp open  http-proxy
8443/tcp open  https-alt
```

详细列表：
```
21/tcp   open  ftp-proxy   Zscaler ftp proxy 6.1
53/tcp   open  domain      (unknown banner: Secured !!! Here no any useful information to you !!!)
| fingerprint-strings:
|   DNSVersionBindReqTCP:
|     version
|     bind
|_    65Secured !!! Here no any useful information to you !!!
| dns-nsid:
|_  bind.version: Secured !!! Here no any useful information to you !!!
80/tcp   open  http        nginx 1.18.0
|_http-title: 502 Bad Gateway
|_http-server-header: nginx/1.18.0
443/tcp  open  https?
554/tcp  open  rtsp?
1723/tcp open  pptp?
|_pptp-version: ERROR: Script execution failed (use -d to debug)
8080/tcp open  http-proxy?
8443/tcp open  https-alt?
```

碰到502：
Ref:
- https://aws.amazon.com/premiumsupport/knowledge-center/load-balancer-http-502-errors/



创建web app部署到tomcat，拿到的文件内容：
### /etc/passwd
```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucp:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
games:x:12:100:games:/usr/games:/sbin/nologin
gopher:x:13:30:gopher:/var/gopher:/sbin/nologin
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin
nobody:x:99:99:Nobody:/:/sbin/nologin
rpc:x:32:32:Rpcbind Daemon:/var/lib/rpcbind:/sbin/nologin
saslauth:x:499:76:"Saslauthd user":/var/empty/saslauth:/sbin/nologin
mailnull:x:47:47::/var/spool/mqueue:/sbin/nologin
smmsp:x:51:51::/var/spool/mqueue:/sbin/nologin
ntp:x:38:38::/etc/ntp:/sbin/nologin
rpcuser:x:29:29:RPC Service User:/var/lib/nfs:/sbin/nologin
nfsnobody:x:65534:65534:Anonymous NFS User:/var/lib/nfs:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
dbus:x:81:81:System message bus:/:/sbin/nologin
ec2-user:x:500:500:EC2 Default User:/home/ec2-user:/bin/bash
nginx:x:498:497:Nginx web server:/var/lib/nginx:/sbin/nologin
apache:x:48:48:Apache:/var/www:/sbin/nologin
xray:x:497:496::/home/xray:/bin/false
tomcat:x:91:91:Apache Tomcat:/usr/share/tomcat8:/sbin/nologin
```

### AWS lambda function渗透
- https://riyazwalikar.github.io/pentestawslambda/#/4
- https://github.com/RhinoSecurityLabs/Cloud-Security-Research/blob/master/AWS/lambda_ssrf/README.md
- [Security Overview of AWS Lambda](https://d1.awsstatic.com/whitepapers/Overview-AWS-Lambda-Security.pdf)
- https://twitter.com/SpenGietz/status/1161317376060563456
- https://medium.com/poka-techblog/privilege-escalation-in-the-cloud-from-ssrf-to-global-account-administrator-fd943cf5a2f6

### lambda
常用命令：
```
printenv
```
查看环境变量

```
LAMBDA_RUNTIME_DIR=/var/runtime
```
![image](https://user-images.githubusercontent.com/30398606/164366443-989000ee-baab-4c56-a171-43c2214292a2.png)

```java
// 拿到某个环境变量
    public static String getEnvOrExit(String envVariableName) {
        String value = System.getenv(envVariableName);
        if (value == null) {
            System.err.println("Could not get environment variable " + envVariableName);
            System.exit(-1);
        }

        return value;
    }
    
    
    private static URL newURL(File parent, String path) {
        try {
            return new URL("file", (String)null, -1, parent.getPath() + "/" + path);
        } catch (MalformedURLException var3) {
            throw new RuntimeException(var3);
        }
    }
    
   
// 设置/var/runtime/lib下的jar包为
    public static URLClassLoader makeRuntimeClassLoader(String runtimePath, ClassLoader parent) {
        List<URL> res = new ArrayList();
        appendJars(new File(runtimePath + "/lib"), res, NO_SORT_ORDER);
        return makeClassLoader(parent, res);
    }
    
    
    private static void appendJars(File dir, List<URL> result, Comparator<String> sortOrder) {
        if (dir.isDirectory()) {
            String[] names = dir.list();
            if (sortOrder != null) {
                Arrays.sort(names, sortOrder);
            }

            String[] var4 = names;
            int var5 = names.length;

            for(int var6 = 0; var6 < var5; ++var6) {
                String path = var4[var6];
                if (path.endsWith(".jar")) {
                    result.add(newURL(dir, path));
                }
            }

        }
    }

    private static URLClassLoader makeClassLoader(ClassLoader parent, List<URL> urls) {
        URL[] allTheUrls = (URL[])urls.toArray(new URL[urls.size()]);
        return new URLClassLoader(allTheUrls, parent);
    }
    
    
    
    public static void main(String[] args) throws Throwable {
        String runtimeDir = getEnvOrExit("LAMBDA_RUNTIME_DIR");
        URLClassLoader internalClassLoader = makeRuntimeClassLoader(runtimeDir, ClassLoader.getSystemClassLoader());
        Class.forName("lambdainternal.AWSLambda", true, internalClassLoader);
    }
```
