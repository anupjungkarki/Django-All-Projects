from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.CharField(max_length=224)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='author')
    date = models.DateField(default=datetime.now())
    liked = models.ManyToManyField('User', default=None, blank=True, related_name='liked')

    def __str__(self):
        return self.content

    @property
    def num_like(self):
        return self.liked.all().count()


LIKE_CHOICES = (
    ('like', 'Like'),
    ('Unlike', 'Unlike'),

)


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=20)

    def __str__(self):
        return str(self.post)


class Profile(models.Model):
    target = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='targets')
