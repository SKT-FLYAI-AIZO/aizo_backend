from account import views
from django.urls import path

app_name = 'account'

urlpatterns = [
    path('', views.AccountView.as_view()),
]
