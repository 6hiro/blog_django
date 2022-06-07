from django.urls import path
from .views import (
    get_profile_comments,
    index,
    portfolio,
    settings,
    contactme_complete,
    ContactmeView,
    RegistrationView,
    LoginView,
    LogoutView,
    VerificationView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    UsernameChangeView,
    delete_account,
    get_profile,
    ProfileChangeView,
)

app_name = 'accounts'

urlpatterns = [
    path('', index, name='home'),
    path('portfolio', portfolio, name='portfolio'),
    path('settings', settings, name='settings'),
    path('contactme', ContactmeView.as_view(), name='contactme'),
    path('contactme/complete', contactme_complete, name='contactme_complete'),
    path('registration/', RegistrationView.as_view(),
         name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/',
         VerificationView.as_view(), name='activate'),
    # change password
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done', PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # reset password
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('username_change', UsernameChangeView.as_view(), name='username_change'),
    path('acccount_delete/<uuid:user_id>',
         delete_account, name='acccount_delete'),
    # profile
    path('profile', get_profile, name='profile'),
    path('profile-comments', get_profile_comments, name='profile_comments'),
    path('profile-change', ProfileChangeView.as_view(), name='profile_change')
]
