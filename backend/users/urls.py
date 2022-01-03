from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate_account/<int:id>/<str:token>/lsfjglsdfjglsdjfgroksjgjsdlglsjertieopsjfgkjsd',
         views.AccountActivationView.as_view(), name='activation_account'),
]
