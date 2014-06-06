from django.contrib import admin
from userprofile.models import UserProfile, PrivateMessage

admin.site.register(UserProfile)
admin.site.register(PrivateMessage)
