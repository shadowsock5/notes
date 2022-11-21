### Ref
- [一些windows命令](https://mp.weixin.qq.com/s/4tyBMIDlaEJ-VgcRvtLUUQ)
- https://yinwc.github.io/2019/08/14/%E5%86%85%E7%BD%91%E6%B8%97%E9%80%8F%E4%B8%8E%E5%90%8E%E6%B8%97%E9%80%8F/
- [Windows blind rce](https://joenibe.github.io/web/Dns-Exfilteration/)

- https://github.com/QAX-A-Team/BrowserGhost
- [红队知识体系梳理-域内信息收集](https://mp.weixin.qq.com/s/FiSh9CaaqXWAWoJErJGgLw)

提取WinSCP，PuTTY等保存的会话信息：

https://github.com/Arvanaghi/SessionGopher

```
wmic process where processid=19656 get processid,caption,executablepath,commandline
```
拿到进程号为19656的进程名，可执行文件路径，命令行。
