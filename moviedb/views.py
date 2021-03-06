import csv
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
import logging
from moviedb.models import Movie, Director
from moviedb.moviescrap import MovieScrap
from django.conf import settings

logger = logging.getLogger(__name__)  # once in each module

# Create your views here.

def index(request):
    movie_list=Movie.objects.all()
    paginator = Paginator(movie_list, 10)
    page=request.GET.get('page')
    try:
        movies=paginator.page(page)
    except PageNotAnInteger:
        movies=paginator.page(1)
    except EmptyPage:
        movies=paginator.page(paginator.num_pages)

    context={'title':'MovieDb','content':movies, 'paginate':True}
    template='moviedb/index.html'
    return render(request, template, context)


def movie_listing(request):
    movies=Movie.objects.all().order_by('title')
    context={'title':'MovieDb','content':movies}
    template='moviedb/movies.html'
    return render(request, template, context)

def director_listing(request):
    directors=Director.objects.order_by('last_name', 'first_name')
    template= 'moviedb/directors.html'
    context={'title':'MovieDb','content':directors}
    return render(request, template, context)


def movie_details(request,movie_id):
    movie=Movie.objects.get(pk=movie_id)
    director=Director.objects.get(pk=movie.director.id)
    related_movies=Movie.objects.filter(director=director.id)
    #
    # IMDB logo
    #
    image = "https://m.media-amazon.com/images/G/01/IMDb/BG_rectangle._CB1509060989_SY230_SX307_AL_.png"
    #
    # Link to imdb page for that movie
    #
    mvs=MovieScrap()
    mvs.setQueryStr(" ".join([movie.title,director.first_name, director.last_name]))
    link = mvs.scrapImdb()
    #
    context={'movie':movie, 'image':image, 'link':link, 'director':director, 'related_movies':related_movies}
    template= 'moviedb/movie_details.html'
    return render(request, template, context)

def director_details(request,director_id):
    director=Director.objects.get(pk=director_id)
    related_movies=Movie.objects.filter(director=director_id)
    #
    # IMDB logo
    #
    image = "https://m.media-amazon.com/images/G/01/IMDb/BG_rectangle._CB1509060989_SY230_SX307_AL_.png"
    #
    # Link to imdb page for that director
    #
    mvs=MovieScrap()
    mvs.setQueryStr(" ".join([director.first_name, director.last_name]))
    link = mvs.scrapImdb()
    context={'director':director, 'image':image, 'link':link, 'related_movies':related_movies}
    template= 'moviedb/director_details.html'
    return render(request, template, context) 

def search(request):
    query=request.GET.get('query')
    if not query:
        movies=Movie.objects.all()
    else:
        movies=Movie.objects.filter(Q(title__icontains=query)
                                |Q(comment__icontains=query)
                                |Q(director__first_name__icontains=query)
                                |Q(director__last_name__icontains=query))
                    
    context={'title':'MovieDb','content':movies}
    template='moviedb/index.html'
    return render(request, template, context)   
        
def export_csv(request):
    movie_list=Movie.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment;filename="moviebase.csv"'

    writer = csv.writer(response,delimiter=';')
    writer.writerow(['First name', 'Last name', 'Title', 'Comment'])
    for m in movie_list:
        writer.writerow([m.director.first_name, m.director.last_name, m.title, m.comment])

    return response
