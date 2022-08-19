import requests

from storage.custom_azure import MyAzureStorage

from django.views import View
from django.http import StreamingHttpResponse


class VideoView(View):
    def get(self, request):
        storage = MyAzureStorage()
        video = storage.open("test_video.mp4", 'r')

        # file_url = 'https://aizoteststorage.blob.core.windows.net/aizo-test-container'
        # r = requests.get(file_url+"/test_video.mp4", stream=True)
        resp = StreamingHttpResponse(streaming_content=video)
        resp['Content-Disposition'] = 'attachment; filename="video.mp4"'

        return resp
