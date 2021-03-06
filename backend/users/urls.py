from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate_account/<int:id>/<str:encrypted_datetime>/<str:token>/',
         views.AccountActivationView.as_view(),
         name='activate_account'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),

    path('change_user_password/', views.ChangePasswordView.as_view(),
         name='change_user_password'),
    path('delete_user_account/', views.DeleteUserAccountView.as_view(),
         name='delete_user_account'),
    path('update_user_data/', views.UpdateUserDataView.as_view(),
         name='update_user_data'),
    path('users_list/', views.UsersListView.as_view(), name='users_list'),
    path('change_user_email/', views.UserChangeEmailView.as_view(),
         name='change_user_email'),
    path('email_confirmation/<int:id>/<str:encrypted_datetime>/<str:token>/',
         views.EmailConfirmationView.as_view(), name='email_confirmation'),
]







