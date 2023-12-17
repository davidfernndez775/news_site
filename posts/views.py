# POST VIEWS
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
# SelectRelatedMixin es una mezcla (mixin) que proporciona la capacidad de realizar consultas select_related para mejorar el rendimiento al recuperar objetos relacionados(ForeignKeys) de la base de datos con una sola consulta.
from braces.views import SelectRelatedMixin
from django.contrib import messages
from . import models
from . import forms
# para ver el usuario actual en User
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    # las Foreign Keys que tiene el modelo a continuacion
    select_related = ('user', 'group')


class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    # algoritmo para buscar los posts en la base de datos que sean del usuario
    def get_queryset(self) -> QuerySet[Any]:
        try:
            self.post_user = User.objects.prefetch_related('posts').get(
                username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.post.all()

    # tomamos el valor de la queryset y lo guardamos en context
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('message', 'group')
    model = models.Post
    # en este caso no se especifica select_related

    # chequeamos la validez del formulario
    def form_valid(self, form):
        # se pone en False para que no pase directamente a la base de datos y poder modificarlo primero
        self.object = form.save(commit=False)
        # establecemos que el autor del post es el usuario logueado
        self.object.user = self.request.user
        # el objeto se guarda en la base de datos
        self.object.save()
        # se termina el proceso de creacion del post
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    # localizamos los post del usuario autenticado en la base de datos
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    # agregamos un mensaje al completar la accion de borrado
    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
