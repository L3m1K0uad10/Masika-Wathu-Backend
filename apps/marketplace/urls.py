from django.urls import path

from .views import (
    CategoryListView,
    ContactClickView
)



urlpatterns = [
    path('categories/', CategoryListView.as_view()),

    path('directory/<int:id>/contact-click/', ContactClickView.as_view()),
]