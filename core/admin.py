from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Notification)
admin.site.register(Report)
admin.site.register(AudioCallPost)
admin.site.register(CallSession)
admin.site.register(CallPost)