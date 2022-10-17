from django.contrib import admin

from .models import Message, Ticket

# Register your models here.


admin.site.register(Message)
admin.site.register(Ticket)
