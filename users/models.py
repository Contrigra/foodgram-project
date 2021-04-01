from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Follow(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')

    class Meta:
        verbose_name = 'Follow list'
        ordering = ('author',)

        constraints = [
            models.UniqueConstraint(fields=('author', 'user',),
                                    name='Unique follow')
            ]

    def __str__(self):
        return f'{self.user} follow list'
