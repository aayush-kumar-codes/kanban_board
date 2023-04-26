from django.urls import path

from .views import BoardView, TaskView


urlpatterns = [
    path('board/', BoardView.as_view()),
    path('board/<int:id>/', BoardView.as_view()),
    path('task/', TaskView.as_view()),
    path('task/<int:id>/', TaskView.as_view())
]
