from django.contrib import admin
from . import models as msg_mod

# Register your models here.
admin.site.register(msg_mod.Message);
admin.site.register(msg_mod.Forum);