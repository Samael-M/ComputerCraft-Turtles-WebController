from django .urls import path
from . import views

app_name = 'controller'
urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name='register'),
    path("register/<uuid:register_link>/", views.register_turtle, name="register_turtle"),
    path("<str:turtle_name>/", views.detail, name="detail"),
]