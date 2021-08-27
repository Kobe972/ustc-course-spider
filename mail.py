from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib
import re
import poplib
poplib._MAXLINE=20480


class Email:

    def __init__(self,account,password,pop3_server):
        self.account = account
        self.password =password
        self.pop3_server = pop3_server

    def guess_charset(self,msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def get_LT(self):
        server = poplib.POP3(self.pop3_server)
        server.user(self.account)
        server.pass_(self.password)
        resp, mails, octets = server.list()
        # 获取最新一封邮件, 注意索引号从1开始:
        index = len(mails)
        resp, lines, octets = server.retr(1)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('ascii')
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        
        value = msg.get('From', '')
        if value:
            hdr, addr = parseaddr(value)
            value = u'%s <%s>' % (hdr, addr)
        else:
            server.quit()
            return None
        if 'GitHub' in value and not msg.is_multipart():
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                result=re.findall('Verification code: (\d{6})',content)
                if len(result)!=0:
                    server.quit()
                    return result[0]
        server.quit()
        return None

