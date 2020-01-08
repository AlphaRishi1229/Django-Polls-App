from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:question_id>/',views.detail,name='detail'),
    path('<int:pk>/results/',views.ResultView.as_view(),name='results'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('create_poll/',views.new_poll,name='new_poll'),
    path('<int:question_id>/create_choice/',views.new_choice,name='new_choice'),
    path('<int:question_id>/review/',views.review,name='review'),
    path('profile/',views.profile,name='profile'),
    path('<int:question_id>/delete/',views.delete,name='delete'),
    path('<int:question_id>/edit/',views.update,name='update'),
    path('<int:question_id>/edit_poll/',views.update_poll,name='update_poll'),
    path('<int:choice_id>/edit_choice/',views.update_choice,name='update_choice'),
    path('<int:choice_id>/delete_choice/',views.delete_choice,name='delete_choice'),
    path('<int:question_id>/change_response/',views.change_response,name='change_response'),
]