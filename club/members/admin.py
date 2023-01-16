from django.contrib import admin
from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class ExerciseAdmin(admin.ModelAdmin):
    # fields = ('user','username','email','phone','photo')
    list_display = ("username",)
    # ordering = ('username',) 