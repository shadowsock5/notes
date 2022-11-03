```java
//        String content = "new java.io.BufferedReader(new java.io.InputStreamReader(Runtime.getRuntime().exec(\"ipconfig\").getInputStream())).readLine()";
        String content = "new String(Runtime.getRuntime().exec(\"ipconfig\").getInputStream().readAllBytes())";

        String result = "";

        /**
         *         Ref: https://github.com/tennc/webshell/blob/9cbc8d5820cd3a83d50fb4ea6bf1c04fd38bd7be/jsp/p2j.cn/readme.md
         *         https://twitter.com/sagar38/status/1115326557269254145
         *         https://twitter.com/pyn3rd/status/1533077054446440450
         *         https://arbitrary-but-fixed.net/teaching/java/jshell/2018/10/18/jshell-exceptions.html
         *         https://mp.weixin.qq.com/s/n1y09ojbHTfFkATsFw-2hQ
         */

        result = jdk.jshell.JShell.create().eval(content).get(0).value().replaceAll("^\"", "").replaceAll("\"$", "");

        System.out.println(result);
```


![image](https://user-images.githubusercontent.com/30398606/199682162-1b8f991a-123a-46b3-89d5-68231057a8fd.png)
