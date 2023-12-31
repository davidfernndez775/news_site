from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from accounts.forms import UserCreateForm
# Create your views here.


class SignUp(CreateView):
    form_class = UserCreateForm
    # se usa reverse_lazy para garantizar que se guarde el signup antes de ir al login
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
