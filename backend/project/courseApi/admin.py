from django.contrib import admin

from .models import Course, Feedback

# Register your models here.

admin.site.register(Course)
admin.site.register(Feedback)  # TODO: remove this later (for development purpose only)
