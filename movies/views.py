from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Movie
from recommendations.models import MovieHistory


def home(request):

    movies = Movie.objects.all()

    # Get search and filter values
    search = request.GET.get('search')
    genre = request.GET.get('genre')
    language = request.GET.get('language')
    city = request.GET.get('city')
    theater = request.GET.get('theater')
    release_date = request.GET.get('release_date')
    show_time = request.GET.get('show_time')
    rating = request.GET.get('rating')
    sort = request.GET.get('sort')

    # Search
    if search:
        movies = movies.filter(
            title__icontains=search
        )

    # Genre filter
    if genre:
        movies = movies.filter(
            genre__iexact=genre
        )

    # Language filter
    if language:
        movies = movies.filter(
            language__iexact=language
        )

    # City filter
    if city:
        movies = movies.filter(
            city__iexact=city
        )

    # Theater filter
    if theater:
        movies = movies.filter(
            theater__iexact=theater
        )

    # Release date filter
    if release_date:
        movies = movies.filter(
            release_date=release_date
        )

    # Show time filter
    if show_time:
        movies = movies.filter(
            show_time=show_time
        )

    # Rating filter
    if rating:
        movies = movies.filter(
            rating__gte=rating
        )

    # Sorting
    if sort == 'rating':

        movies = movies.order_by(
            '-rating'
        )

    elif sort == 'newest':

        movies = movies.order_by(
            '-release_date'
        )

    elif sort == 'popularity':

        movies = movies.order_by(
            '-popularity'
        )

    elif sort == 'price_low':

        movies = movies.order_by(
            'ticket_price'
        )

    elif sort == 'price_high':

        movies = movies.order_by(
            '-ticket_price'
        )

    # Count movies after applying filters
    movie_count = movies.count()

    # Pagination
    paginator = Paginator(
        movies,
        6
    )

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(
        page_number
    )

    # Keep filters when changing pages
    query_params = request.GET.copy()

    query_params.pop(
        'page',
        None
    )

    return render(
        request,
        'movies/home.html',
        {
            'movies': page_obj,
            'movie_count': movie_count,
            'page_obj': page_obj,
            'query_params': query_params
        }
    )


def movie_detail(request, movie_id):

    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    # Save movie history for logged-in users
    if request.user.is_authenticated:

        MovieHistory.objects.create(
            user=request.user,
            movie=movie
        )

    return render(
        request,
        'movies/movie_detail.html',
        {
            'movie': movie
        }
    )