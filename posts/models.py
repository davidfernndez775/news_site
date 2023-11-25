from collections.abc import Iterable
from django.db import models
from django.conf import settings
# para direccionamiento
from django.urls import reverse
import misaka
from groups.models import Group
from django.contrib.auth import get_user_model
User = get_user_model  # nopep8


# Create your models here.
# POST MODELS

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    # el auto_now=True permite que el sistema ponga la fecha y la hora automaticamente en el post
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(
        Group, related_name='posts', null=True,  blank=True)

    def __str__(self) -> str:
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post:single", kwargs={'username': self.user.username, "pk": self.pk})

    class Meta:
        # definimos el orden en el que queremos ver los posts
        ordering = ['-created_at']
        # definimos una pareja de elementos que juntos deben ser unicos, por ejemplo a cada mensaje le corresponde un solo usuario
        unique_together = ['user', 'message']
