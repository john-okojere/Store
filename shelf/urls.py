from django.urls import path
from . import views

urlpatterns = [
    path("",views.homepage , name="homepage"),
    path("about",views.about , name="about"),
    path("faq",views.FAQ , name="faq"),
    path("returnPolicy",views.returnPolicy , name="return-policy"),
    path("deliveryPolicy",views.deliveryPolicy , name="delivery-policy"),
    path("privacyPolicy",views.privacyPolicy , name="privacy-policy"),
    path("Terms-&-Condition",views.TermsCondition , name="TermsCondition"),
    path("contact",views.contact , name="contact"),
    path("details/<uuid:uid>",views.details , name="details"),

    path("add-product", views.add_product, name="add-product"),
    path("edit-product/<uuid:uid>", views.edit_product, name="edit-product"),

    path('filter/', views.filter_items, name='filter_items'),
    
    path('search', views.search, name="search"),
    path('ss', views.search_suggestions, name="search_suggestions" ),
    path('category/<str:cat>', views.category_view, name="category"),
]