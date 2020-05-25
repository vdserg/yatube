from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_post, name="new_post"),
    path("group/<slug:slug>/", views.group_posts, name="group_posts"),
    path("<username>/", views.profile, name="profile"),
    path("<username>/<int:post_id>/", views.post_view, name="post"),
    path("<username>/<int:post_id>/edit/", views.post_edit,
         name="post_edit")
]
