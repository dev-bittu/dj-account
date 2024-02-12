from django.contrib import admin
from .models import User, ConfirmEmail

# Register your models here.
admin.site.register(User)
admin.site.register(ConfirmEmail)
