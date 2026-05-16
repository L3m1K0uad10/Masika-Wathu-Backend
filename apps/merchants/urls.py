from django.urls import path

from .views import (
    DirectoryListView,
    DirectoryDetailView,
    MerchantProfileView,
    MerchantImageUploadView,
    VerificationUploadView,
    MerchantStatsView
)



urlpatterns = [
    path('directory/', DirectoryListView.as_view()),

    path('directory/<slug:slug>/', DirectoryDetailView.as_view()),

    path('merchant/profile/', MerchantProfileView.as_view()),

    path('merchant/images/', MerchantImageUploadView.as_view()),

    path('merchant/verify/', VerificationUploadView.as_view()),

    path('merchant/stats/', MerchantStatsView.as_view()),
]