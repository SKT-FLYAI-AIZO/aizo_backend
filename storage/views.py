from datetime import datetime

import requests
from azure.storage.blob import BlobServiceClient
from django.http import JsonResponse
from django.views import View

from account.models import Account
from aizo_backend.settings import STORAGE_CONNECTION_STRING, MEDIA_URL, TMAP_APP_KEY
from media.models import Video
from storage.custom_azure import MyAzureStorage

my_storage = MyAzureStorage()


class VideoUploaderView(View):
    def post(self, request):
        video_file = request.FILES.get('video_file')
        if video_file is None:
            return JsonResponse({"message": "There is no video file..."}, status=400)

        loc = request.POST.get('loc')
        if loc is None:
            return JsonResponse({"message": "There is no loc..."}, status=400)

        email = request.POST.get('email')
        if email is None:
            return JsonResponse({"message": "There is no email..."}, status=400)

        date = request.POST.get('date')
        if date is None:
            return JsonResponse({"message": "There is no date..."}, status=400)

        video_filename = str(email) + "_" + date + ".mp4"

        try:
            blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
            blob_video_client = blob_service_client.get_blob_client(container=my_storage.azure_container, blob=video_filename)
            blob_video_client.upload_blob(video_file, overwrite=True)

        except Exception as e:
            return JsonResponse({"message": "Upload failed", "message": str(e)}, status=400)

        query = Account.objects.filter(email=email).only("id")
        if query.__len__() == 0:
            return JsonResponse({"message": "There is no such email."}, status=204)
        account_id = int(query.get().id)

        pred_param = {"user_id": account_id,
                      "path": video_filename,
                      "gps_file": loc,
                      "date": date
                      }

        APP_KEY = TMAP_APP_KEY
        GEO_API_URL = "https://apis.openapi.sk.com/tmap/geo/reversegeocoding"

        pred_response = requests.post("http://test-aizo.azurewebsites.net/play", data=pred_param)

        pred_path_list = pred_response.json().get('path')
        gps = pred_response.json().get('gps')

        for i in range(len(pred_path_list)):
            lat = gps[i].get('lat')
            lon = gps[i].get('lon')

            if lat is None or lon is None:
                return JsonResponse({"message": "There is no lat or lon"}, status=400)

            geo_param = {"version": 1, "lat": lat, "lon": lon}
            geo_header = {"appKey": APP_KEY}

            geo_response = requests.get(GEO_API_URL, headers=geo_header, params=geo_param)

            if geo_response.status_code == 200:
                address_info = geo_response.json().get("addressInfo")
                full_address = address_info.get("fullAddress")
            elif geo_response.status_code == 204:
                full_address = "Unknown location"
            else:
                return JsonResponse({"message": "Geo api error"}, status=400)

            Video.objects.create(
                date=datetime.strptime(' '.join(date.split('-')), '%Y %m %d'),
                location=full_address,
                account_id_id=account_id,
                path=pred_path_list[i],
                is_cropped=True
            ).save()

        Video.objects.create(
            date=datetime.strptime(' '.join(date.split('-')), '%Y %m %d'),
            location="test location",
            account_id_id=account_id,
            path=MEDIA_URL + video_filename
        ).save()

        return JsonResponse({"message": "Success!"}, status=201)
