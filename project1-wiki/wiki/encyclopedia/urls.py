from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.content_page, name="content_page"),
    path("search", views.show_search_results, name="show_search_results"),
    path("add", views.add_entry, name="add_entry"),
    path("edit", views.edit_entry, name="edit_entry"),
    path("random/", views.random_page, name="random_page"),
]
