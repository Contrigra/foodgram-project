from django.urls import path

from users.views import sign_up_view
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
urlpatterns = [
    path('signup', sign_up_view, name='sign_up'),
    # path('password_change', password_change_view, name='password_change',),
    # path('password_reset', password_reset_view, name='password_reset'),
    # path('password_reset', PasswordResetView.as_view(
    #     template_name='registration/password_reset_form.html'),
    #      name='password_reset'),
# #     path('accounts/password/reset/', PasswordResetDoneView.as_view(
# #         template_name='registration/password_reset_done.html'),
# #          name='password_reset_done'),
# #     path('accounts/password/reset/', PasswordResetConfirmView.as_view(
# #         template_name='registration/password_reset_confirm.html'),
# #          name='password_reset_confirm'),
# #     path('accounts/password/reset/', PasswordResetCompleteView.as_view(
# #         template_name='registration/password_reset_comlete.html'),
# #          name='password_reset_complete'),
]
