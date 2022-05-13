from django.urls import path
from .views import SubjectListView, SubjectDetailView


urlpatterns = [
    path('/<int:pk>',SubjectDetailView.as_view()),
    path('',SubjectListView.as_view())
]