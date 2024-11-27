from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("product/<int:pk>/", views.product, name="product"),
    path("categories/<str:name>/", views.category, name="category"),
    path("search/", views.search, name="search"),
]
