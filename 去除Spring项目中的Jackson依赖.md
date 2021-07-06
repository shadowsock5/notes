`spring-boot-starter-web`和`spring-boot-starter-actuator`都会引入`jackson-databind`。

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
            <exclusions>
                <exclusion>
                    <groupId>com.fasterxml.jackson.core</groupId>
                    <artifactId>jackson-databind</artifactId>   <!-- 排除掉jackson -->
                </exclusion>
            </exclusions>
        </dependency>
```
需要手动将其排除掉。

```
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>    <!-- 这个会引入jackson -->
            <exclusions>
                <exclusion>
                    <groupId>com.fasterxml.jackson.core</groupId>
                    <artifactId>jackson-databind</artifactId>   <!-- 排除掉jackson -->
            </exclusions>
        </dependency>
```
