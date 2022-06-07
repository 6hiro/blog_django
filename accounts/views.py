from unicodedata import category
from django.http import HttpResponse, JsonResponse
from urllib.request import HTTPRedirectHandler
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views import View
from django.core.mail import send_mail, BadHeaderError
from articles.models import Category, Post
from django.conf import settings as conf_settings
from django.contrib.auth.decorators import login_required

from .forms import (
    MyPasswordResetForm, MySetPasswordForm
)
from .models import Profile
from .utils import EmailUtil, account_activation_token


def index(request):
    # posts = Post.objects.all()
    categories = Category.objects.all()
    for_range = [i for i in range(10)]

    context = {
        "categories": categories,
        "for_range": for_range,
    }
    return render(request, 'home.html', context)


# @login_required
def portfolio(request):
    return render(request, 'portfolio.html')


@login_required
def settings(request):
    context = {
        "user": request.user,
        # "username": request.user.name
    }
    return render(request, 'settings.html', context)


def contactme_complete(request):
    return render(request, 'contactme_complete.html')


class ContactmeView(View):
    def get(self, request):
        return render(request, 'contactme.html')

    def post(self, request):
        subject = request.POST.get('subject', None)
        username = request.POST.get('username', None)
        sender = request.POST.get('email', None)
        text = request.POST.get('text', None)
        body = text + "\n by " + username + "(" + sender + ")"
        try:
            # print('######')
            email = EmailMessage(
                subject=str(subject), body=str(body), from_email=str(sender), to=[conf_settings.EMAIL_HOST_USER])
            email.send()
            # send_mail(subject=subject, message=text, from_email=sender,
            #           recipient_list=[conf_settings.EMAIL_HOST_USER])
        except BadHeaderError:
            return HttpResponse
        return redirect('accounts:contactme_complete')


def registration(request):
    return render(request, 'accounts/registration.html')


class RegistrationView(View):
    def get(self, request):
        return render(request, 'accounts/registration.html')

    def post(self, request):
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)

        context = {
            'username': username,
            'email': email
        }
        if get_user_model().objects.filter(username=username).exists():
            messages.error(request, '既にこのアカウント名が存在します')
            return render(request, 'accounts/registration.html', context)

        if not get_user_model().objects.filter(email=email).exists():
            if len(password) < 7:
                messages.error(request, 'パスワードを７字以上にしてください')
                return render(request,  'accounts/registration.html', context)
            if password != repassword:
                messages.error(request, 'パスワードとパスワード確認は同じ値を入力してください')
                return render(request,  'accounts/registration.html', context)

            user = get_user_model().objects.create_user(
                username=username, email=email, password=password)
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            link = reverse('accounts:activate', kwargs={
                'uidb64': uid,
                'token': token
            })

            activate_url = 'http://' + current_site.domain + link
            email_body = user.email + \
                'さん、ご登録ありがとうございます。\nメールアドレスに間違いがなければ、以下のリンクからログインしてください。 \n' + activate_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'ユーザー登録を完了してください'}
            EmailUtil.send_email(data)
            messages.success(request, '確認メールを送信しました')
            return render(request, 'accounts/registration.html')

        messages.error(request, '既にアカウントが存在します')
        return render(request, 'accounts/registration.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                redirect('/login')

            if user.is_verified:
                return redirect('/login')

            user.is_verified = True
            user.save()
            Profile.objects.create(user=user, nick_name='ななしさん')

            messages.success(request, 'アカウント作成が完了しました')
            return redirect('/login')
        except Exception as e:
            # print(e)
            pass

        return redirect('/login')


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        context = {
            'email': request.POST.get('email', None)
        }

        if password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                messages.error(request, 'ユーザー登録が完了していません\nメールを確認してください')
                return render(request, 'accounts/login.html')

            messages.error(request, 'メールアドレスまたは、パスワードが間違っています')
            return render(request, 'accounts/login.html', context)
        messages.error(request, 'すべての項目を入力してください')
        return render(request, 'accounts/login.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'ログアウトが完了しました')
        return redirect('/login')


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'

    # def get_context_data(self, **kwargs):
    #     context =  super().get_context_data(**kwargs)
    #     context['form_name'] = 'password_change'
    #     return context


class PasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class PasswordResetView(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'accounts/mail_template/password_reset/subject.txt'
    email_template_name = 'accounts/mail_template/password_reset/message.txt'
    template_name = 'accounts/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDoneView(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetCompleteView(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'accounts/password_reset_complete.html'


@login_required
def edit_account_username(request, user_id):
    if request.user.id == user_id:
        username = request.POST.get('username', None)
        user = get_user_model().objects.get(id=user.id).update(username=username)
    return redirect('/login')


class UsernameChangeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/username_change.html')

    def post(self, request):
        username = request.POST.get('username', None)

        if username:
            if get_user_model().objects.filter(username=username).exists():
                messages.error(request, '既にこのアカウント名が存在します')
                return render(request, 'accounts/username_change.html')
            if len(username) > 20:
                messages.error(request, '20字以内で入力してください')
                return render(request, 'accounts/username_change.html')

            get_user_model().objects.filter(id=request.user.id).update(username=username)
            return redirect('/settings')

        messages.error(request, 'ユーザーネームを入力してください')
        return render(request, 'accounts/username_change.html')


@login_required
def delete_account(request, user_id):

    if request.user.id == user_id:
        try:
            user = get_user_model().objects.filter(id=user_id).first()
            user.delete()
            return redirect('/login')
        except:
            # return JsonResponse({'error': 'error'})
            return redirect('/settings')

    return redirect('/settings')


@login_required
def get_profile(request):
    profile = Profile.objects.get(user=request.user)
    favorite_posts = request.user.favorite_post.all()
    context = {
        'profile': profile,
        'favorite_posts': favorite_posts,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def get_profile_comments(request):
    profile = Profile.objects.get(user=request.user)
    comments = request.user.user_comment.all()
    context = {
        'profile': profile,
        'comments': comments,
    }
    return render(request, 'accounts/profile_comments.html', context)


class ProfileChangeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/profile_change.html')

    def post(self, request):
        nick_name = request.POST.get('nickName', None)

        if nick_name:
            if len(nick_name) > 20:
                messages.error(request, '20字以内で入力してください')
                return render(request, 'accounts/profile_change.html')

            Profile.objects.filter(user_id=request.user.id).update(
                nick_name=nick_name)
            return redirect('/profile')

        messages.error(request, 'ニックネームを入力してください')
        return render(request, 'accounts/profile_change.html')
