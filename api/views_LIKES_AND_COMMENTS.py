from rest_framework import permissions
from rest_framework.generics import ListAPIView

from FORM_MSG.models import Like, Comment
from api.serializers import LikeSerializerSIMPLE2, CommentSerializer


class LikeListView(ListAPIView):
    """Likes"""
    queryset = Like.objects.select_related('user', 'message').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializerSIMPLE2


class CommentList(ListAPIView):
    queryset = Comment.objects.select_related('user', 'message').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
