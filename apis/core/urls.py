
from django.urls import include, path


from core.views import (
    Home,
    MovieDetailView
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("movie-detail/<int:movie_id>/",
         MovieDetailView.as_view(), name="movie_details"),
]
