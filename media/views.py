import json

import requests
from rest_framework.permissions import IsAuthenticated

from media.models import Video
from media.serializers import VideoSerializer

from django.views import View
from django.http import StreamingHttpResponse, JsonResponse


class VideoView(View):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        id = request.GET.get('id')
        account_id = request.GET.get('account_id')

        if id:              # 특정 비디오 하나만 가져오는 경우, id는 Video 테이블의 id
            queryset = Video.objects.filter(id=id)
        elif account_id:    # 특정 유저의 모든 비디오를 가져오는 경우
            queryset = Video.objects.filter(account_id=account_id).order_by('-date')
        else:               # video 테이블의 모든 비디오를 가져오는 경우
            queryset = Video.objects.all()

        serializer = VideoSerializer(queryset, many=True)
        data = serializer.data

        return JsonResponse({"message": "Success!", "data": data}, safe=False)

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

        return JsonResponse({"message": "Video Saved!"}, status=200)


class FileView(View):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        file_url = request.GET.get('path')
        r = requests.get(file_url, stream=True)
        response = StreamingHttpResponse(streaming_content=r)
        response['Content-Disposition'] = 'attachment; filename="video.mp4"'

        return response
