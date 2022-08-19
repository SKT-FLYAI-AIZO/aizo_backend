from media import views
from django.urls import path

app_name = 'media'

urlpatterns = [
    path('', views.VideoView.as_view()),
]