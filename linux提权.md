Ref：
- https://gtfobins.github.io/#+suid

```
find / -perm -u=s -type f 2>/dev/null
```



### sudosers
```
echo "test_user ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/test_user
```
ref:
- https://developers.redhat.com/blog/2018/08/15/how-to-enable-sudo-on-rhel
- https://myexperiments.io/linux-privilege-escalation.html
