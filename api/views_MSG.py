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
    permission_classes = (permissions.AllowAny,)
    ordering_fields = ['-created_date']

class MessagesViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'patch', 'head', 'delete')  # option
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)  # (permissions.AllowAny,)

    queryset = Message.objects.all().prefetch_related("author")

    serializer_class = MsgSerializer

    def perform_create(self, serializer):
        if self.request.user:
            serializer.save(author=self.request.user)
        else:
            # 401 unauthorized
            return Response(status=status.HTTP_401_UNAUTHORIZED)
