from django.contrib import admin
from django.urls import include, path
from controller import views as controller_views

urlpatterns = [
    path('', controller_views.index, name='home'),  # Direct root URL to index view
    path("controller/", include("controller.urls")),
    path("admin/", admin.site.urls),
]
