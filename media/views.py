import json

import requests
from rest_framework.permissions import IsAuthenticated

from account.models import Account
from media.models import Video
from media.serializers import VideoSerializer

from django.views import View
from django.http import JsonResponse, HttpResponse


class VideoView(View):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        id = request.GET.get('id')
        email = request.GET.get('email')

        if id:              # 특정 비디오 하나만 가져오는 경우, id는 Video 테이블의 id
            queryset = Video.objects.filter(id=id, is_cropped=True)
        elif email:         # 특정 유저의 모든 비디오를 가져오는 경우
            query = Account.objects.filter(email=email).only("id")
            if query.__len__() == 0:
                return JsonResponse({"message": "There is no such email."}, status=204)
            account_id = int(query.get().id)
            queryset = Video.objects.filter(account_id=account_id, is_cropped=True).order_by('-date')
        else:               # video 테이블의 모든 비디오를 가져오는 경우
            queryset = Video.objects.all(is_cropped=True)

        if queryset.__len__() == 0:
            return JsonResponse({"message": "There is no video."}, status=204)

        serializer = VideoSerializer(queryset, many=True)
        data = serializer.data

        return JsonResponse({"message": "Success!", "data": data}, safe=False, status=200)

    # 테스트용 더미데이터 생성 API
    def post(self, request):
        serializer = VideoSerializer(data=json.loads(request.body))
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        Video.objects.create(
            account_id=data['account_id'],
            date=data['date'],
            location=data['location'],
            path=data['path']
        ).save()

        return JsonResponse({"message": "Video Saved!"}, status=201)


class FileView(View):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        file_url = request.GET.get('path')
        idx = file_url.rfind('/')
        file_name = file_url[idx:]

        r = requests.get(file_url, stream=True)
        response = HttpResponse(r.content, content_type="video/mp4")
        response['Content-Disposition'] = 'inline; filename="{}"'.format(file_name)

        return response
