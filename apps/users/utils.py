from django.core.mail import send_mail
from django.conf import settings
import random
import string


def generate_confirmation_code():
    return ''.join(random.choices(string.digits, k=4))


def send_confirmation_code_to_user(user, code):
    subject = 'Soffwork.uz | Tasdiqlash Kodingiz'
    message = f'Sizning soffwork.uz uchun tasdiqlash kodingiz: {code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error while sending email: {str(e)}")


def send_verification_code_to_user(phone, code):
    print(f"Verification code: {str(code)}")
    # message_id = str(timezone.now())  # noqa
    # requests.post(
    #     settings.SMS_URL,
    #     auth=(settings.SMS_LOGIN, settings.SMS_PASSWORD),
    #     json={
    #         "messages": [
    #             {
    #                 "recipient": str(phone),
    #                 "message-id": message_id,
    #                 "sms": {
    #                     "originator": "3700",
    #                     "content": {
    #                         "text": f"soffwork.uz <#> Sizning tasdiqlash kodingiz {code}"
    #                     },
    #                 },
    #             }
    #         ]
    #     },
    # )


