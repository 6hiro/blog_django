from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # user.is_active, user.pk, timestamp は text_typeしてもしなくても値が変わらない
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))

# PasswordResetTokenGeneratorのままでもメール確認によるユーザー登録は機能する
# account_activation_token = PasswordResetTokenGenerator()
account_activation_token = TokenGenerator()


class EmailUtil:
    # インスタンス化せずに呼び出せる関数（第一引数にselfを受け取らない）
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()