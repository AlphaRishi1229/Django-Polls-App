from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/',views.DetailView.as_view(),name='detail'),
    path('<int:pk>/results/',views.ResultView.as_view(),name='results'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('create_poll/',views.new_poll,name='new_poll'),
    path('<int:question_id>/create_choice/',views.new_choice,name='new_choice'),
    path('<int:question_id>/review/',views.review,name='review'),
]