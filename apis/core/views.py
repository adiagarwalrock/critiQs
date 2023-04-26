import requests
from api.models import Comment
from .forms import (
    CommentForm,
    CustomUserCreationForm,
)

from django.conf import settings
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth import get_user_model
User = get_user_model()


API_KEY = settings.MOVIE_API_KEY


class Home(TemplateView):

    context_object_name = "popular_movies"
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        pages = [1, 2]
        result = []
        for i in pages:
            url = "https://api.themoviedb.org/3/movie/popular?api_key="+API_KEY + \
                "&language=en-US&page="+str(i)+"&append_to_response=videos"
            try:
                try:
                    response = requests.get(url,
                                            timeout=5,
                                            headers={'Content-Type': 'application/json'})
                except requests.Timeout:
                    response = None
                if not response or response.status_code != 200:
                    response = requests.get(url,
                                            timeout=5,
                                            headers={'Content-Type': 'application/json'})
                    if response.status_code != 200:
                        return None
            except (ConnectionError, requests.Timeout):
                return None

            result += response.json()['results'][:len(response.json()
                                                      ['results'])-1]

        kwargs['carousel'] = result[:5]
        kwargs['genres'] = settings.GENERES
        kwargs['popular_movies'] = result[5:]
        return super().get_context_data(**kwargs)


def get_cast(movie_id: int):
    url = "https://api.themoviedb.org/3/movie/"+movie_id + \
        "/credits?api_key="+API_KEY+"&language=en-US"
    response = requests.get(url,
                            timeout=5,
                            headers={'Content-Type': 'application/json'})

    return response.json()['cast']


def get_similar(movie_id: int):
    url = "https://api.themoviedb.org/3/movie/"+movie_id + \
        "/similar?api_key="+API_KEY+"&language=en-US&page=1"
    response = requests.get(url,
                            timeout=5,
                            headers={'Content-Type': 'application/json'})

    return response.json()['results']


class MovieDetailView(CreateView):
    model = Comment
    template_name = 'movie_detail.html'
    form_class = CommentForm

    def get_context_data(self, *args, **kwargs):
        movie_id = str(self.kwargs['movie_id'])
        comments = Comment.objects.filter(content_id=movie_id)
        url = "https://api.themoviedb.org/3/movie/"+movie_id + \
            "?api_key="+API_KEY+"&language=en-US"
        try:
            try:
                response = requests.get(url,
                                        timeout=5,
                                        headers={'Content-Type': 'application/json'})
            except requests.Timeout:
                response = None
            if not response or response.status_code != 200:
                response = requests.get(url,
                                        timeout=5,
                                        headers={'Content-Type': 'application/json'})
                if response.status_code != 200:
                    return None
        except (ConnectionError, requests.Timeout):
            return None

        kwargs['movie'] = response.json()
        kwargs['genres'] = settings.GENERES
        kwargs['credits'] = get_cast(movie_id)
        kwargs['similar'] = get_similar(movie_id)
        kwargs['comments'] = comments

        return super().get_context_data(**kwargs)

    def post(self, request, **kwargs):
        # method to post a movie comment to the database
        if request.method == 'POST':
            request.POST._mutable = True
            movie_id = self.kwargs['movie_id']
            comment = request.POST.get('body')

            request.POST['content_id'] = movie_id
            request.POST['user'] = self.request.user
            request.POST._mutable = False
            print(request.POST)
            form = CommentForm()
            print(form)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)

        return super(MovieDetailView, self).post(request, **kwargs)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"
