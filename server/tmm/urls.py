from django.urls import path

from .views import (
  CreateUserMailView,
  GetUserMailView,
  GetUserMailsView,
)

urlpatterns = [
  path('create', CreateUserMailView.as_view()),
  path('get/all', GetUserMailsView.as_view()),
  path('get/mail', GetUserMailView.as_view())
]