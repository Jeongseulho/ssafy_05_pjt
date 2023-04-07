from django.shortcuts import render
from django.views.decorators.http import (require_http_methods, require_POST,
                                          require_safe)

from .models import Movie

# Create your views here.


@require_safe
def index(req):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(req, 'movies/index.html', context)
