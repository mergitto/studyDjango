from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # 例: /polls/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'), # 例: /polls/1
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'), # 例: /polls/1/results
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'), # 例: /polls/1/vote
]
