from random import Random
from users.models import EmailCode
from django.core.mail import send_mail
from PythonMxOnline.settings import EMAIL_FROM


# 随机验证码
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_email(email, send_type="register"):
    emailCode = EmailCode()
    code = random_str(16)
    emailCode.code = code
    emailCode.email = email
    emailCode.send_type = send_type
    emailCode.save()

    email_title = ""
    email_message = ""
    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_message = "请点击下面的链接来激活您的账号：http://127.0.0.1:8000/active/{0}".format(code)

        is_send_email = send_mail(email_title, email_message, EMAIL_FROM, [email])
        if is_send_email:
            pass
    elif send_type == "forget":
        email_title = "慕学在线网重置密码链接"
        email_message = "请点击下面的链接来重置密码：http://127.0.0.1:8000/reset/{0}".format(code)

        is_send_email = send_mail(email_title, email_message, EMAIL_FROM, [email])
        if is_send_email:
            pass

