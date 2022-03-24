### transient
```
就是让某些被修饰的成员属性变量不被序列化
```

> 为什么要不被序列化呢，主要是为了节省存储空间，其它的感觉没啥好处，可能还有坏处（有些字段可能需要重新计算，初始化什么的），总的来说，利大于弊。


参考：
- https://www.cnblogs.com/chenpi/p/6185773.html


- [JAVA安全基础（一）--类加载器（ClassLoader）](https://xz.aliyun.com/t/9002)
