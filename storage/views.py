import json
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

        idx = date.rfind(".")
        remake_date = date[:idx]
        remake_date = remake_date.replace("T", "_")

        video_filename = str(email) + "_" + remake_date + ".mp4"

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

        try:
            if type(loc) != str:
                raise TypeError
            loc = json.loads(loc)
            loc_dict = {"data": {}}
            for item in loc['data']:
                loc_dict["data"][item['time']] = [item['lat'], item['lon']]
        except TypeError:
            return JsonResponse({"message": "loc type error"}, status=400)
        except Exception as e:
            return JsonResponse({"message": "make loc failed" + str(e)}, status=400)

        pred_param = {"path": video_filename, "gps": loc_dict, "time": date}

        pred_param = json.dumps(pred_param, ensure_ascii=False, separators=(',', ':'))

        APP_KEY = TMAP_APP_KEY
        GEO_API_URL = "https://apis.openapi.sk.com/tmap/geo/reversegeocoding"
        HEADER = {"Content-Type": "application/json"}
        pred_response = requests.post("http://20.214.150.23:9090/play", headers=HEADER, json=pred_param, timeout=3600)

        if pred_response.status_code != 200:
            return JsonResponse({"message": "pred api error", "res_content": str(pred_response.content)}, status=400)

        pred_path_list = pred_response.json().get('path')
        gps = pred_response.json().get('gps')
        date_list = pred_response.json().get('date')

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
                date=date_list[i],
                location=full_address,
                account_id_id=account_id,
                path=pred_path_list[i],
                is_cropped=True
            ).save()

        Video.objects.create(
            date=date,
            location="원본 영상은 위치정보 X",
            account_id_id=account_id,
            path=MEDIA_URL + video_filename
        ).save()

        return JsonResponse({"message": "Success!"}, status=201)
