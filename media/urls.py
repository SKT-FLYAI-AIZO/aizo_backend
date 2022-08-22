from media import views
from django.urls import path

app_name = 'media'

urlpatterns = [
    path('/video', views.VideoView.as_view()),
    path('/file', views.FileView.as_view())
]