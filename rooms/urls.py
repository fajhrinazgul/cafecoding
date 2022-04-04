from django.urls import path 
from rooms import views

app_name = "rooms"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("room/<str:slug>/", views.RoomDetailView.as_view(), name="room_detail"),
    path("join/<int:pk>/<str:username>/", views.join_room, name="join_room"),
    path("quit/<int:pk>/<str:username>/", views.quit_room, name="quit_room"),
    path("search/", views.RoomSearchListView.as_view(), name="search"),
    path("edit/<str:pk>/", views.RoomUpdateFormView.as_view(), name="room_edit"),
]