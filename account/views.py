# import mixin as mixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework import status, mixins, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import MyUser
from account.permissions import IsUserPermission
from account.serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully signed up!", status=status.HTTP_201_CREATED)


class ActivateView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(MyUser, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response("Your account successfully activated!", status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        print(user)
        Token.objects.filter(user=user).delete()
        return Response("Successfully logged out", status=status.HTTP_200_OK)


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'
    lookup_url_kwarg = 'email'
    lookup_value_regex = '[\w@.]+'

    def get_permissions(self):
        if self.action in ['retrieve', 'partial_update', 'destroy', 'update']:
            permissions = [IsAuthenticated, IsUserPermission, ]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}
