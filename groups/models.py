from django.db import models
# permite hacer mas legible el direccionamiento web
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model  # nopep8
from django import template  # nopep8
register = template.Library()  # nopep8

# Create your models here.
# GROUPS MODELS

# clase que crea los grupos


class Group(models.Model):
    # definimos un nombre único para cada grupo
    name = models.CharField(max_length=255, unique=True)
    # definimos el slug
    slug = models.SlugField(allow_unicode=True, unique=True)
    # definimos una descripción
    description = models.TextField(max_length=500, blank=True, default='')
    #
    description_html = models.TextField(editable=False, default='', blank=True)
    #
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self) -> str:
        return self.name

    # hace el slug al nombre cuando se guarda la instancia
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)


# clase que identifica a los miembros de un grupo


class GroupMember(models.Model):
    # relaciona al miembro con el grupo
    group = models.ForeignKey(Group, related_name='memberships')
    # relaciona al miembro con el usuario
    user = models.ForeignKey(User, related_name='user_groups')

    # devuelve el nombre del usuario referenciado al atributo username de la clase User
    def __str__(self) -> str:
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
