from django.contrib import admin
from rooms.models import Room

class RoomAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("title",),
    }
    
admin.site.register(Room, RoomAdmin)