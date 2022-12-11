from django.conf import settings
from django.contrib.auth import get_user_model

from django.db import models
from django.urls import reverse
from django.db.models import Avg
#from django.contrib.auth.models import User

class Article(models.Model):
    username = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='pictures')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("article_detail", args=[str(self.id)])


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",  # new
    )
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("article_list")

    
class Review(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="reviews" # new
    )
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    comment = models.TextField(max_length = 250)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.comment)

    def get_absolute_url(self):
        return reverse('article_new', args=[str(self.id)])

    @property
    def avg(self,author1):
        average = Review.objects.aggregate(Avg('rate'))
        return average

