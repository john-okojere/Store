from django.urls import path
from . import views

urlpatterns = [
    path("",views.homepage , name="homepage"),
    path("about",views.about , name="about"),
    path("contact",views.contact , name="contact"),
    path("details/<uuid:uid>",views.details , name="details"),
    path("add-product", views.add_product, name="add-product"),

    path('filter/', views.filter_items, name='filter_items'),
    
    path('search', views.search, name="search"),
    path('ss', views.search_suggestions, name="search_suggestions" ),
    path('category/<str:cat>', views.category_view, name="category"),
]