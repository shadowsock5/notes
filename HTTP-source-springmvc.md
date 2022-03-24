# Spring中的常用注解

- Spring Framework的注解（跟HTTP请求没关系）
- Spring Boot的注解（）
- Spring MVC的注解

### Ref

- https://www.java67.com/2019/04/top-10-spring-mvc-and-rest-annotations-examples-java.html
- https://www.javadevjournal.com/spring-mvc/spring-mvc-annotations/
- https://docs.spring.io/spring-framework/docs/3.2.x/spring-framework-reference/html/mvc.html
- https://www.baeldung.com/spring-mvc-annotations

#### 其他参考
- [Spring Framework Annotations](https://www.javadevjournal.com/spring/spring-annotations/)
- [Spring Boot Annotations](https://www.javadevjournal.com/spring-boot/spring-boot-annotations/)

### Annotations

- @Controller：是一种特殊的@Component，它告诉Spring IOC容器将这个注解标示的类当作一个Spring MVC的Controller
- @PathVariable：路径变量
- @RequestParam：请求参数
- @RequestBody：将HTTP的入口数据，转换成Java对象
- @ResponseBody：（对应地）将Java对象，转换成响应数据
- @RequestMapping：将HTTP请求与Java方法进行映射，有这些属性：consumes, produces, method, header, name, value
- @GetMapping, @PostMapping是@RequestMapping 加上一些属性的简写
- @RestController：相当于@Controller + @ResponseBody。如果不用这个，就得在类上注解@Controller，然后在每个方法中都注解@ResponseBody
- @SprinbBootApplication：相当于@Configuration + @EnableAutoConfiguration + @ComponentScan
- @ResponseStatus：复写HTTP响应的状态码
- @ModelAttribute：分两种形式：方法参数级别，和方法级别。
- @PreAuthorize：碰到的一个鉴权的注解，支持SpEL表达式。
- @RequestHeader("User-Agent")


参考：
方法参数级别的@ModelAttribute
```java
@PostMapping("/saveInvoice")
public String saveInvoice(@ModelAttribute("invoice") Invoice invoice) {
            // Code that uses the invoice object to save it
           // service.saveInvoice(invoice);
      return "invoiceListView";
}
```
方法级别的@ModelAttribute
```java
@ModelAttribute
public void includeAttributes(Model model) {
       model.addAttribute("message", "additional attribute to all methods");
}
```
可以添加全局的model attribute，并且，被@ModelAttribute注解的的方法，是在所有的@RequestMapping or even @GetMapping  and @PostMapping注解的方法被调用之前被调用。


### 示例
```java
// nodeMemberService是一个NodeMemberService对象，通过@Autowired引入。
    @RequestMapping("/xxx.do/{nodeId}")
    @PreAuthorize("@nodeMemberService.isOwnerOfNodeOrSuperAdmin(#nodeId)")
    @ResponseBody
    public DefaultResponse xxx(@PathVariable("nodeId") Long nodeId,
                                                         @RequestParam Long groupId,
                                                         HttpServletRequest request)
                                                         ...
                                                         }
```

在进入xxx方法之前，会调用nodeMemberService这个isOwnerOfNodeOrSuperAdmin方法，参数为用户传入的nodeId。
