from django.urls import path, include
from .import views

# all url routes
urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name="register"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('user/', views.AuthUserAPIView.as_view(), name="user"),
    path('users/', views.UserListAPIView.as_view(), name="user-list"),
    path('filter/', views.UserSearchFilterAPIView.as_view(), name="user-filter"),
    path('users/update/<int:pk>', views.UpdateUserAPIView.as_view(), name="update"),
]