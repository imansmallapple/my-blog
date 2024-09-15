from users.models import EmailVerifyRecord
from django.core.mail import send_mail
import random
import string


def random_str(randomlength=8):
    chars = string.ascii_letters+string.digits
    strcode = ''.join(random.sample(chars, randomlength))
    return strcode


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = "Blog's registration active link"
        email_body = 'Please click the following link to activate the account: http://51.20.54.201:8000//users/active/{0}'.format(code)
        # main code of sending the email
        send_status = send_mail(email_title, email_body, 'alf138540fun@gmail.com', [email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = "find password link"
        email_body = 'Please click the following link to reset your password: http://127.0.0.1:8000/users/forget_pwd_url/{0}'.format(code)
        # main code of sending the email
        send_status = send_mail(email_title, email_body, 'alf138540fun@gmail.com', [email])
        if send_status:
            pass