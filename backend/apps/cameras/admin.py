from django.contrib import admin
from .models import Camera


# Register your models here.
@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ["camera_id", "location", "source_url"]
