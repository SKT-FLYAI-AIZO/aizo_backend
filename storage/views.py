from datetime import datetime

import requests
from azure.storage.blob import BlobServiceClient
from django.http import JsonResponse
from django.views import View

from aizo_backend.settings import STORAGE_CONNECTION_STRING, MEDIA_URL
from media.models import Video
from storage.custom_azure import MyAzureStorage

my_storage = MyAzureStorage()


class VideoUploaderView(View):
    def post(self, request):
        video_file = request.FILES.get('video_file')
        if video_file is None:
            return JsonResponse({"message": "There is no video file..."}, status=400)

        loc_file = request.FILES.get('loc_file')
        if loc_file is None:
            return JsonResponse({"message": "There is no loc file..."}, status=400)

        account_id = request.POST.get('account_id')
        location = request.POST.get('location')
        date = request.POST.get('date')

        if account_id is None or location is None or date is None:
            return JsonResponse({"message": "Check info"}, status=400)

        video_filename = str(account_id) + "_" + str(location) + "_" + str(date) + ".mp4"
        loc_filename = str(account_id) + "_" + str(location) + "_" + str(date) + ".txt"

        try:
            blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
            blob_video_client = blob_service_client.get_blob_client(container=my_storage.azure_container, blob=video_filename)
            blob_loc_client = blob_service_client.get_blob_client(container=my_storage.azure_container, blob=loc_filename)

            blob_video_client.upload_blob(video_file, overwrite=True)
            blob_loc_client.upload_blob(loc_file, overwrite=True)
        except Exception:
            return JsonResponse({"message": "Upload failed"}, status=400)

        Video.objects.create(
            date=datetime.strptime(' '.join(date.split('-')), '%Y %m %d'),
            location=location,
            account_id_id=int(account_id),
            path=MEDIA_URL + video_filename
        ).save()

        return JsonResponse({"message": "Success!"}, status=200)
