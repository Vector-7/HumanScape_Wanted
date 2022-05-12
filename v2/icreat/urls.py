from django.urls import path
from v1.icreat.views import SubjectListView, SubjectDetailView


urlpatterns = [
    path('<int:pk>',SubjectDetailView.as_view()),
    path('/list',SubjectListView.as_view())
]