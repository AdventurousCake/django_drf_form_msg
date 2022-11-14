from django.urls import path
from . import views

app_name = 'form_msg'

# NOT DRF API
urlpatterns = [
    path('send/', views.send_msg, name='send_msg'),
    path('edit/<int:pk>/', views.edit_msg, name='edit_msg'),
    path('delete/<int:pk>/', views.delete_msg, name='delete_msg'),
    path('', views.msg_list, name='msg_list'),
    path('<int:pk>/', views.get_msg, name='show_msg'),


    path("signup/", views.SignUp.as_view(), name="signup"),
    path("users/<int:pk>/", views.UserDetails.as_view(), name="users_details"),

]