from django.core.mail import send_mail
from django.conf import settings
import random
import string
import requests
from django.utils import timezone


def generate_confirmation_code():
    first_digit = random.choice(string.digits[1:])  # 1 dan 9 gacha
    other_digits = ''.join(random.choices(string.digits, k=3))  # 3 ta raqam
    return first_digit + other_digits


def send_confirmation_code_to_user(user, code):
    subject = 'Tasdiqlash Kodingiz'
    message = f'Sizning tasdiqlash kodingiz: {code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error while sending email: {str(e)}")


def send_verification_code_to_user(phone, code):
    pass
    # print(f"Verification code: {str(code)}")
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
    #                         "text": f" <#> Sizning tasdiqlash kodingiz {code}"
    #                     },
    #                 },
    #             }
    #         ]
    #     },
    # )