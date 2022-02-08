from django.urls import path
from . import views


app_name = 'challenges'
urlpatterns = [
    path('create_challenge/', views.CreateChallengeView.as_view(),
         name='create_challenge'),
    path('upload_video_example/<int:challenge_id>/',
         views.UploadVideoExampleView.as_view(), name='upload_video_example'),
    path('accept_challenge/<int:challenge_id>/',
         views.AcceptChallengeView.as_view(), name='accept_challenge'),
]
