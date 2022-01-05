from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate_account/<int:id>/<str:token>/',
         views.AccountActivationView.as_view(),
         name='activate_account'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('change_password/', views.ChangePasswordView.as_view(),
         name='change_password'),
    path('users_list/', views.UsersListView.as_view(), name='users_list'),
]
