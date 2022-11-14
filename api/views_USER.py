from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import UserSerializer, UserSerializerSIMPLE
from core.models import User


class UserViewSet(ModelViewSet):
    """users_vset/ get by id"""
    queryset = User.objects.all().prefetch_related('messages')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserViewSetRO(ReadOnlyModelViewSet):
    """alt users ReadOnlyModelViewSet; ТОЛЬКО RETRIEVE AND LIST"""
    queryset = User.objects.all()
    serializer = UserSerializer


class UserList(APIView):
    """users_view/ get by username
    global permissions dep; необходимо каждый раз передавать token, получив через auth"""
    permission_classes = (permissions.AllowAny,)

    def get(self, request, username):
        # ПОЛЯ В СЕРИАЛИЗАТОРЕ!
        # users = User.objects.values('id', 'username', 'messages').select_related('messages').filter(username=username)
        # users = User.objects.select_related('messages').filter(username=username) # select_related: 'messages'. Choices are: auth_token

        users = User.objects.select_related().prefetch_related('messages').filter(username=username)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
