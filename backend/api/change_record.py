from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView
from django.db.models import Q

from backend.utils.page import Page
from repository import models
from backend.cmdbSerializers.common_serializers import AssetRecord


class ChangeRecord(ViewSetMixin, APIView):
    queryset = models.AssetRecord.objects.all().order_by('-create_at')
    serializer_class = AssetRecord
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        creator = request.query_params.get('creator')
        if creator != '1':  # 查手动修改的记录
            self.queryset = self.queryset.filter(creator_id=None)
        else:
            self.queryset = self.queryset.filter(~Q(creator_id=None))
        response = {'code': 20000, 'msg': None, 'data': None}
        # device_status_id = int(request.query_params.get('device_status_id'))
        page = Page()
        total = self.queryset.count()
        page_list = page.paginate_queryset(self.queryset, request, view=self)
        # print(request.META.get('REMOTE_ADDR'))
        instance = page_list
        ser_record = self.serializer_class(instance=instance, many=True)
        response['data'] = ser_record.data
        response['msg'] = 'successful'
        response['total'] = total
        return Response(response)
