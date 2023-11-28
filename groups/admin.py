from django.contrib import admin
from . import models

# Register your models here.

# El tabularinline nos permite desde el sitio de administracion modificar la clase GroupMember desde la clase Group, por tanto no tenemos que registrarla


class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember


admin.site.register(models.Group)
