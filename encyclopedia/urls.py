from django.urls import path, re_path
from . import util
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<entry>", views.entry_page, name="entry"),
    path("search/", views.search_page, name="search"),
    path("random/", views.random_page, name="random"),
    path("new/", views.input_page, {'title': "New Page", 'new': True}, name="new"),
    path("edit/<title>", views.input_page, {'new': False}, name="edit")
]