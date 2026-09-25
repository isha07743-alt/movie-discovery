from django.db import models


class Movie(models.Model):

    title = models.CharField(max_length=200)

    genre = models.CharField(max_length=100)

    language = models.CharField(max_length=50)

    city = models.CharField(max_length=100)

    theater = models.CharField(max_length=200)

    release_date = models.DateField()

    rating = models.FloatField(default=0)

    ticket_price = models.FloatField(default=0)

    show_time = models.TimeField()

    popularity = models.IntegerField(default=0)

    def __str__(self):
        return self.title