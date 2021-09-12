from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('user/list/', views.UserListView.as_view(), name='user_list'),
    path('user/add/', views.UserCreateView.as_view(), name='user_add'),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
]
