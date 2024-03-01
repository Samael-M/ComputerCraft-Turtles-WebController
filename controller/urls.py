from django .urls import path
from . import views

app_name = 'controller'
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("<str:turtle_name>/", views.detail, name="detail"),
]