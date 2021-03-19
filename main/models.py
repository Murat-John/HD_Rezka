from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

MyUser = get_user_model()


class Genre(models.Model):
    image = models.ImageField(upload_to='genre_image')
    slug = models.SlugField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    premiere = models.DateTimeField(auto_now=True)
    budget = models.PositiveIntegerField()
    poster = models.ImageField(upload_to='poster')
    created = models.DateTimeField(auto_now_add=True)
    movie = models.FileField(upload_to='movie')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)


class MovieImage(models.Model):
    image = models.ImageField(upload_to='movie_image')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}\t {self.created}\n\t{self.text}"

    class Meta:
        ordering = ('-created',)


class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)


class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)


class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(default=0)


class History(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='histories')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='histories')
    created = models.DateTimeField(auto_now_add=True, blank=True)