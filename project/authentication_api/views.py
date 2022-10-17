import random

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import (ChangePasswordSerializer, RegisterSerializer,
                          UpdateProfileSerializer)


class RegisterView(generics.CreateAPIView):
    """
    post:
        Create a new user. Returns created post data.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    put:
        calls Django Auth SetPassword save method.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    """
    put:
        update an existing user main information.
        Default accepted fields: username, first_name, last_name.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer


class UpdateUserImageView(APIView):
    """
    put:
        update an existing user image.
    """
    parser_classes = (MultiPartParser, )
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, format=None):
        user = request.user
        if user.pk != pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={
                'detail': {
                    "authorize": "you dont have permission for this user !",
                    },
                })
        if 'image' in request.data:
            profile = get_object_or_404(Profile, pk=pk)
            profile.image = request.data['image']
            profile.user = user
            profile.save()
            return Response(
                status=status.HTTP_200_OK, data={"detail": 'modified'})

        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': {'not-valid': 'the image field data is missing'}})


class LogoutView(APIView):
    """
    post:
        Calls Django logout method and delete the Token object
        assigned to the current User object.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteProfileView(APIView):
    """
    Delete:
        Delete an existing user.
    """
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk, format=None):
        user = request.user
        if user.pk != pk:
            return Response(
                data={"detail": "unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED)

        if 'password' not in request.data:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'detail': 'password-required'})

        if not user.check_password(request.data['password']):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'detail': "password-incorrect"})

        user.is_active = False
        user.save()
        return Response(status=status.HTTP_200_OK, data={"detail": "deleted"})


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        if not 'email' or 'username' in request.data:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'detail': {'email_or_username': 'required'}})

        user = None
        if 'email' in request.data:
            user = get_object_or_404(User, email=request.data['email'])
        if 'user' in request.data:
            user = get_object_or_404(User, username=request.data['username'])
        mail_subject = 'Reset Your Password'
        server_code = random.randint(10000, 999999)
        message = 'Hi {0},\nthis is your email confirmation code:\n{1}'.format(user.first_name,
                                                                               server_code)

        to_email = user.email
        EmailMessage(mail_subject, message, to=[to_email]).send()
        request.session['code'] = server_code
        request.session['user'] = user.username
        return Response(status=status.HTTP_200_OK, data={'detail': "sent"})


class ResetPasswordView(APIView):
    """
    put:
        Calls Django Auth PasswordResetForm save method.
        Accepts the following POST parameters: email
        Returns the success/fail message.
    """
    permission_classes = (AllowAny,)

    def put(self, request, pk, format=None):
        user = get_object_or_404(User, username=request.session['user'])
        if user.pk != pk:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"detail": "unauthorized"})

        if not 'password' and 'again' in request.data:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'detail': {"password": "required", 'again': 'required'}})

        if request.data['password'] != request.data['again']:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': 'not-matched'})

        user.set_password(request.data['password'])
        user.save()
        return Response(status=status.HTTP_200_OK, data={'detail': 'done'})
