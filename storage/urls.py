from storage import views
from django.urls import path

app_name = 'storage'

urlpatterns = [
    path('/video-uploader', views.VideoUploaderView.as_view()),
]
