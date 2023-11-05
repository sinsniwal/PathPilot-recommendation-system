from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import POD, CustomUser, Student


class UserAgentAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    ADDITIONAL_USER_FIELDS = ((None, {"fields": ("user_type",)}),)
    fieldsets = fieldsets + ADDITIONAL_USER_FIELDS

    list_filter = (
        "first_name",
        "last_name",
    )


admin.site.register(CustomUser, UserAgentAdmin)
admin.site.register(Student)
admin.site.register(POD)
