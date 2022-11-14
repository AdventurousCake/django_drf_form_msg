from django.http import JsonResponse
from rest_framework import permissions, filters, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsOwnerOrReadOnly
from api.serializers import MsgSerializer
# from rest_framework.decorators import action

from FORM_MSG.models import Message


# msg_load/ # for js
class MsgLoadView(APIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # paginator
        messages = Message.objects.all()

        # OR serializers.ListSerializer FOR MANY=TRUE
        serializer = MsgSerializer(messages, many=True)

        text = {
            'status': 'ok',
            'data': serializer.data
        }
        return JsonResponse(text)


# GET http://127.0.0.1:8000/api/v1/msg_search/?search=123
# GET http://127.0.0.1:8000/api/v1/msg_search/?text=236263
# viewset с фильтром и поиском
class MsgSearchViewSet(ModelViewSet):
    queryset = Message.objects.all()

    serializer_class = MsgSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', ]  # 'name'
    permission_classes = (permissions.AllowAny,)  # (permissions.IsAuthenticatedOrReadOnly,)
    ordering_fields = ['-created_date']


# !!! MAIN MSG /msg; viewset - multiple actions
# class ModelViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet)
class MessagesViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'patch', 'head', 'delete')  # option
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)  # (permissions.AllowAny,)
    # throttle_classes = [UserRateThrottle]
    # throttle_scope = 'low_request'

    # queryset = Message.objects.all() # not optimal for author field
    # queryset = Message.objects.all().select_related("author").prefetch_related("groups", "user_permissions") # invalid parameters in prefetch
    # queryset = Message.objects.all().select_related("author").prefetch_related("author.groups", "author.user_permissions") # invalid parameters in prefetch

    # queryset = Message.objects.all().select_related("author")  # not optimal for author fields fk
    queryset = Message.objects.all().prefetch_related("author")

    # FOR ALL USER DATA; UNDERSCORE in fields
    # queryset = Message.objects.all().select_related("author").prefetch_related("author__groups", "author__user_permissions")

    serializer_class = MsgSerializer

    # PERFORM CREATE находится внутри create, после валидации(is_valid)! check overrides
    def perform_create(self, serializer):
        if self.request.user:
            serializer.save(author=self.request.user)
        else:
            # 401 unauthorized
            return Response(status=status.HTTP_401_UNAUTHORIZED)

            # # can be User instance
            # serializer.save(author='unknown')  # str for ONLY str field


    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    # def create(self, response, *args, **kwargs):
    #     response['data'] = {}
    #     return Response(response, status=status.HTTP_401_UNAUTHORIZED)
