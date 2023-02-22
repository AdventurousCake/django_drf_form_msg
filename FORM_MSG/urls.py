from django.urls import path

from FORM_MSG import views, views_likes

app_name = 'form_msg'

urlpatterns = [
    path('send/', views.MsgFormCreateView.as_view(), name='send_msg'),
    path('edit/<int:pk>/', views.UpdateMsgView.as_view(), name='edit_msg'),
    path('delete/<int:pk>/', views.DeleteMsgView.as_view(), name='delete_msg'),
    path('', views.MsgList.as_view(), name='msg_list'),

    path('<int:pk>/', views.DetailMsgANDCommentView.as_view(), name='show_msg'),
    path('like/<int:pk>/', views_likes.UpdateLikeView.as_view(), name='like'),  # dj


    path("signup/", views.SignUp.as_view(), name="signup"),
    path("users/<int:pk>/", views.UserDetails.as_view(), name="users_details"),

]