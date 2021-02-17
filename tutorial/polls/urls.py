from django.urls import path

from . import views

app_name = 'polls' # To differentiate URL names between apps
urlpatterns = [
    # path(path after polls, view in views.py, name)
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
