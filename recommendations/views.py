from django.shortcuts import render
from .models import MovieHistory
from movies.models import Movie


def recommendations(request):

    recommended_movies = Movie.objects.none()
    recently_viewed = Movie.objects.none()

    if request.user.is_authenticated:

        history = MovieHistory.objects.filter(
            user=request.user
        ).select_related('movie').order_by('-viewed_at')

        # Recently Viewed Movies
        recently_viewed_ids = list(
            history.values_list('movie_id', flat=True)[:6]
        )

        recently_viewed = Movie.objects.filter(
            id__in=recently_viewed_ids
        )

        # Recommended Movies
        if history.exists():

            latest_movie = history.first().movie

            recommended_movies = Movie.objects.filter(
                genre__iexact=latest_movie.genre
            ).exclude(
                id=latest_movie.id
            ).order_by('-rating')[:6]

    return render(
        request,
        'recommendations/recommendations.html',
        {
            'recommended_movies': recommended_movies,
            'recently_viewed': recently_viewed
        }
    )