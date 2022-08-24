from datetime import datetime

from azure.storage.blob import BlobServiceClient
from django.http import JsonResponse
from django.views import View

from account.models import Account
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

        email = request.POST.get('email')
        location = request.POST.get('location')
        date = request.POST.get('date')

        if email is None or location is None or date is None:
            return JsonResponse({"message": "Check info. Fill all data."}, status=400)

        video_filename = str(email) + "_" + str(location) + "_" + str(date) + ".mp4"
        loc_filename = str(email) + "_" + str(location) + "_" + str(date) + ".txt"

        try:
            blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
            blob_video_client = blob_service_client.get_blob_client(container=my_storage.azure_container, blob=video_filename)
            blob_loc_client = blob_service_client.get_blob_client(container=my_storage.azure_container, blob=loc_filename)

            blob_video_client.upload_blob(video_file, overwrite=True)
            blob_loc_client.upload_blob(loc_file, overwrite=True)
        except Exception:
            return JsonResponse({"message": "Upload failed"}, status=400)

        query = Account.objects.filter(email=email).only("id")
        account_id = int(query.get().id)

        Video.objects.create(
            date=datetime.strptime(' '.join(date.split('-')), '%Y %m %d'),
            location=location,
            account_id_id=account_id,
            path=MEDIA_URL + video_filename
        ).save()

        return JsonResponse({"message": "Success!"}, status=200)
