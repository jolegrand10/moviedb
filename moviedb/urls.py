from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name ='index'),
    url(r'^export_csv$', views.export_csv, name ='export_csv'),
    url(r'^movie$', views.movie_listing,name='movie_listing'),
    url(r'^director$', views.director_listing,name='director_listing'),
    url(r'^director/(?P<director_id>[0-9]+)$', views.director_details, name='director_details'),
    url(r'^movie/(?P<movie_id>[0-9]+)$', views.movie_details, name='movie_details'),
    url(r'^search/$', views.search, name='search'),

]
