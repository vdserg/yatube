from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

urlpatterns = [
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("site-admin/", admin.site.urls),
    path("about/", include("django.contrib.flatpages.urls")),
    path("about-author/", views.flatpage, {"url": "/about-author/"},
         name="author"),
    path("about-spec/", views.flatpage, {"url": "/about-spec/"}, name="spec"),
    path("", include("posts.urls")),
]
