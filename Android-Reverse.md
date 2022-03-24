版本低，强制升级才能使用
- WEB接口的HTTP请求头（比如UA）
- AndroidManifest.xml中的android:versionCode值
- 注释掉弹出对话框的smali代码，回编译
- 查找网上的第一版，往往安全性不够(可能需解决强制更新问题)



tips:
查找某目录下的所有文本文件中，并将待替换字符串换成指定字符串：

```bash
grep -rl ‘src_str’ ./ |xargs sed -i “” “s/src_str/new_str/g”
```


Hook：
- Frida
- Xposed

## Ref
- http://www.520monkey.com/archives/1384
