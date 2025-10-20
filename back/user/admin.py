from django.contrib import admin
from user.models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "gender"]


admin.site.register(UserInfo, UserInfoAdmin)
