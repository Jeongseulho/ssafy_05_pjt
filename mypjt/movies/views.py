from django.shortcuts import redirect, render
from django.views.decorators.http import (require_http_methods, require_POST,
                                          require_safe)

from .forms import MovieForm
from .models import Movie


@require_safe
def index(req):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(req, 'movies/index.html', context)


@require_http_methods(['GET', 'POST'])
def create(req):
    if req.method == 'POST':
        # 파일 및 이미지는 req.FILES에 담기므로 이것도 넘겨줘야함
        form = MovieForm(req.POST, req.FILES)
        if form.is_valid() and req.user.is_authenticated:
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()

    context = {'form': form}
    return render(req, 'movies/create.html', context)


@require_safe
def detail(req, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie': movie
    }
    return render(req, 'movies/detail.html', context)


@require_http_methods(['GET', 'POST'])
def update(req, pk):
    movie = Movie.objects.get(pk=pk)
    if req.method == 'POST':
        form = MovieForm(req.POST, instance=movie)
        if form.is_valid() and req.user.is_authenticated:
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'form': form,
        'movie': movie
    }

    return render(req, 'movies/update.html', context)


@require_POST
def delete(req, pk):
    if req.user.is_authenticated:
        movie = Movie.objects.get(pk=pk)
        movie.delete()
    return redirect('movies:index')
