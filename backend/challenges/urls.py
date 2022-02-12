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
    path('get_challenges_list/', views.GetChallengesListView.as_view(),
         name='get_challenges_list'),
    path('get_detail_challenge/<int:challenge_id>/',
         views.GetDetailChallenge.as_view(), name='get_detail_challenge'),
    path('get_challenge_members/<int:challenge_id>/',
         views.GetChallengeMembers.as_view(), name='get_challenge_members'),
    path('add_answer_on_challenge/<int:challenge_id>/',
         views.AddAnswerOnChallenge.as_view(), name='add_answer_on_challenge'),
]
