from django.db import models
# permite hacer mas legible el direccionamiento web
from django.utils.text import slugify
import misaka
# para direccionamiento
from django.urls import reverse
# el metodo get_user_model identifica al usuario que esta registrado y lo conecta a la clase User
from django.contrib.auth import get_user_model
User = get_user_model  # nopep8
# todavia no entiendo la importacion del template
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
    # descripcion del markdown text
    description_html = models.TextField(editable=False, default='', blank=True)
    # definimos todos los miembros que pertenecen a este grupo
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        '''funcion que mejora la visualidad en la direccion del navegador'''
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        '''funcion por defecto para cuando termine de crear un post vaya a una url determinada, se sustituye la PrimaryKey por el slug'''
        return reverse("groups:single", kwargs={"slug": self.slug})

    class Meta:
        # definimos el orden en que queremos ver los grupos
        ordering = ['name']


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
        # definimos una pareja de elementos que juntos deben ser unicos, por ejemplo en cada grupo no pueden haber dos usuarios con el mismo nombre
        unique_together = ('group', 'user')
