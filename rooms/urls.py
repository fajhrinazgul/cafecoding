from django.urls import path 
from rooms import views

app_name = "rooms"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("room/<str:slug>/", views.RoomDetailView.as_view(), name="room_detail"),
    path("join/<int:room_pk>/<str:username>/", views.join_room, name="join_room"),
    path("accepted_join/<int:room_pk>/<str:username>/", views.join_room_accepted, name="join_room_accepted"),
    path("rejected_join/<int:room_pk>/<str:username>/", views.join_room_rejected, name="join_room_rejected"),
    path("quit/<int:room_pk>/<str:username>/", views.quit_room, name="quit_room"),
    path("accepted_quit/<int:room_pk>/<str:username>/", views.quit_room_accepted, name="quit_room_accepted"),
    path("rejected_quit/<int:room_pk>/<str:username>/", views.quit_room_rejected, name="quit_room_rejected"),
    path("search/", views.RoomSearchListView.as_view(), name="search"),
    path("edit/<str:pk>/", views.RoomUpdateFormView.as_view(), name="room_edit"),
]