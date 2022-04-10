from django.contrib import admin
from rooms.models import Room, AuthenticatedJoinQuitRoom

class RoomAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("title",),
    }
    
admin.site.register(Room, RoomAdmin)
admin.site.register(AuthenticatedJoinQuitRoom)