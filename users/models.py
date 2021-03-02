from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Follow(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
