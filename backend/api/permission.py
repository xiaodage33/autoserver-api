from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView

from backend.utils.page import Page
from repository import models
from backend.cmdbSerializers.common_serializers import PermissionSerializer
# from django.contrib.auth import models


class Permission(ViewSetMixin, APIView):
    queryset = models.Permission.objects.all()
    serializer_class = PermissionSerializer
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        response = {'code': 20000, 'msg': None, 'data': None}
        # device_status_id = int(request.query_params.get('device_status_id'))
        # print(request.META.get('REMOTE_ADDR'))
        ser_permission = self.serializer_class(instance=self.queryset, many=True)
        response['data'] = ser_permission.data
        response['msg'] = 'successful'
        return Response(response)
