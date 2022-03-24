## 静态代码审计

- [java AST 抽象语法树-JavaParser 框架](https://houbb.github.io/2020/05/29/java-ast-01-javaparser)
- [JavaParse(AST)获取Java Web API list](https://mp.weixin.qq.com/s/ATpoEN9QI-D5vkxDimQ8FQ)
- https://gist.github.com/B1ueB0ne/7ee600305364f76bf5105c98054f62e6
- [使用javalang进行AST分析](https://blog.riskivy.com/%e4%bb%8east%e5%88%b0100%e4%b8%aa%e6%9f%90%e7%9f%a5%e5%90%8doa%e5%89%8d%e5%8f%b0%e6%b3%a8%e5%85%a5/)
- [如何将SAST融入DevSecOps流程中？](https://mp.weixin.qq.com/s/ye77l3mWoJcCYiL1ShByVw)
- [DevSecOps: How to Seamlessly Integrate Security Into DevOps](https://cdn2.hubspot.net/hubfs/1958393/White_Papers/devsecops_how_to_seamlessly__315283.pdf)
- [Gitlab集成Sonarqube实现自动检测代码并发送报告给提交者](https://www.cnblogs.com/xiaozi/p/15102003.html)

## 白盒扫描技术综述
- [白盒扫描技术综述](https://anemone.top/whitebox-%E7%99%BD%E7%9B%92%E6%89%AB%E6%8F%8F%E6%8A%80%E6%9C%AF%E7%BB%BC%E8%BF%B0/)

![image](https://user-images.githubusercontent.com/30398606/138552340-49b732d7-1543-44ae-9ce0-cc89c278c6d8.png)
![image](https://user-images.githubusercontent.com/30398606/138552375-da71e03d-80d8-4a43-ad31-fa4267c10690.png)

概括就是：
1、无法处理“黑盒子”。比如容器类型，或者黑盒方法，无法解析内部如何处理，放进去的是污染的，但是拿出来的是否是污染的，就无法确定，导致过污染或者欠污染；
2、难以分析“清洁函数”（sanitizer）；
3、难以分析“控制流”（if false; rce）
4、难以处理特殊污染条件（与具体漏洞原理有关，比如SSRF能控制host才算漏洞）


## SDL

- [应用安全评审中的三个关键节点及抓手实现](https://mp.weixin.qq.com/s/g22EJQRPjrlzL165lcB6AA)
- [SDL安全与企业办公安全落地实践](https://mp.weixin.qq.com/s/B4Oh8QG_BR4Z8s3U6Bc6Uw)
- [SDL软件安全设计初窥](https://xz.aliyun.com/t/41/)


### 主要工作
- 1、建立安全编码规范
- 2、静态源代码安全分析
- 3、开源组件安全扫描（OSS）
- 4、安全过滤库&中间件



常见java安全过滤库：`ESAPI`
- https://github.com/ESAPI/esapi-java-legacy
- https://www.cnblogs.com/fishou/p/4177491.html


静态代码扫描工具：
[a FindBugs and SpotBugs plugin for doing static code analysis on java byte code](https://github.com/mebigfatguy/fb-contrib)


交互应用安全测试: `security_taint_propagation`
污点分析？

https://github.com/cdaller/security_taint_propagation


## 动态插桩


## SAST融入Devsecops的不同场景

### 场景1. IDE研发阶段检测

- 使用场景：将SAST集成到开发人员的IDE中，在开发人员键入代码时保存时，进行检测
- 目的：在代码被提交到代码仓库之前发现修补并最常见的的安全问题，帮助代码研发人员在研发阶段发现缺陷
- 检测耗时：秒级
- 规则集：低误报的检测项，偏规则类，主要采用函数内分析技术

对于部分检测器无法确定的问题，SAST工具在预提交检测时会选择暂时不报出漏洞，避免给开发人员增加额外的负担。

### 场景2. 提交时检测

- 使用场景：代码提交至代码仓库后自动触发
- 目的：每次提交的结果快速返回给提交代码的开发人员
- 检测耗时：分钟级
- 规则集：可选有限检测项

与IDE检测不同的是，在该阶段会关注跨函数，跨文件的缺陷类型。

### 场景3. 构建时检测

- 使用场景：代码提交成功并编译后，定时进行检测
- 目的：每天定时反馈问题
- 检测耗时：小时级
- 规则集：允许配置更全面的检测项，例如OWASP Top 10 


### 场景4. 测试时检测

- 使用场景：成功构建后在环境中进行全量检测
- 目的：将构建好的软件部署到模拟环境中，进行全量测试
- 检测耗时：数小时级
- 规则集：全部检测项

SAST检测结果将由QA进行分析和评估。
