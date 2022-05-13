from django.urls import path

from .views import IcreatBatchView

urlpatterns = [
    path('', IcreatBatchView.as_view())
]