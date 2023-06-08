from django.urls import path

from caseworker.bookmarks import views

app_name = "bookmarks"

urlpatterns = [
    path("add", views.AddBookmark.as_view(), name="add_bookmark"),
    path("delete", views.DeleteBookmark.as_view(), name="delete_bookmark"),
    path("rename", views.RenameBookmark.as_view(), name="rename_bookmark"),
]
