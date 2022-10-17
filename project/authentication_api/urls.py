from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (ChangePasswordView, DeleteProfileView, ForgotPasswordView,
                    LogoutView, RegisterView, ResetPasswordView,
                    UpdateProfileView, UpdateUserImageView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('change_image/<int:pk>/', UpdateUserImageView.as_view(), name='auth_image'),
    path('delete_profile/<int:pk>/', DeleteProfileView.as_view(), name='auth_delete_profile'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='auth_forgot_password'),
    path('reset_password/<int:pk>', ResetPasswordView.as_view(), name='auth_reset_password'),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]