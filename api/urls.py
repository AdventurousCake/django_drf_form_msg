from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views_LIKES_AND_COMMENTS import LikeListView, CommentList
from .views_MSG import MessagesViewSet, MsgSearchViewSet, MsgLoadView
from .views_USER import UserViewSet, UserList

app_name = 'api'

# APPEND_SLASH=False
router = DefaultRouter()
router.register('msg', MessagesViewSet)
router.register('msg_search', MsgSearchViewSet)

# You cannot add generic Views in routers
# router.register('msg_load', MsgLoadView, basename="Message")

router.register('users_vset', UserViewSet)

urlpatterns = [
    # ROUTER VSETS
    path('', include(router.urls)),

    path('msg_load/', MsgLoadView.as_view(), name='msg_load'),
    path('users_view/<str:username>/', UserList.as_view(), name='msg_user'),
    path('likes_list', LikeListView.as_view(), name='likes_list'),
    path('comments_list', CommentList.as_view(), name='comments_list'),

    path('api-token-auth/', views.obtain_auth_token),

    # swagger and schema
    path('swagger', TemplateView.as_view(template_name='api/swagger-ui.html',
                                         extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    path('openapi', get_schema_view(
            title="My Project",
            description="API for all things …",
            version="1.0.0",
            permission_classes=(permissions.AllowAny,),
            # public=True,
        ), name='openapi-schema'),

]

# JWT
urlpatterns += [
    path('jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
