
from django.urls import include, path


from core.views import (
    Home,
    MovieDetailView,
    SignUpView,
    TvSeriesDetailView,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("movie-detail/<int:movie_id>/",
         MovieDetailView.as_view(), name="movie_details"),

    path("series-detail/<int:series_id>",
         TvSeriesDetailView.as_view(), name="series_details"),

    path("signup/", SignUpView.as_view(), name="signup"),
]
