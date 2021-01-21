from django.core.mail import send_mail


def send_activation_mail(email, activation_code):
    print(activation_code)
    subject = 'Account activation'
    message = f'Чтобы активировать ваш аккаунт перейдите по ссылке: http://127.0.0.1:8000/accounts/activate/{activation_code}'
    from_ = 'test@test.com'
    emails = [email, ]

    send_mail(subject, message, from_, emails, fail_silently=True)