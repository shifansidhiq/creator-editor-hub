from django.contrib import admin

# Register your models here.
from .models import user_login, user_details

from.models import user_login
from.models import user_details,creator_details, user_report


admin.site.register(user_login)
admin.site.register(user_details)
admin.site.register(creator_details)
admin.site.register(user_report)
