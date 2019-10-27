from repository import models

from rest_framework.response import Response
from backend.test.cmdb_serializers import ServerSerializer

# Create your views here.


from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from api.utils.token import get_token


# from rest_framework.viewsets import ModelViewSet


# class Server(APIView):
#     def get(self, request):
#         # servers = models.Server.objects.all()
#         servers = models.Asset.objects.all()
#         ser_servers = ServerSerializer(servers, many=True)
#         # print(ser_servers,type(ser_servers))
#         # print(ser_servers.data,type(ser_servers.data))
#         return Response(ser_servers.data)
#
#     def post(self, request):
#         ser_server = ServerSerializer(data=request.data)
#         if ser_server.is_valid():
#             print(ser_server.validated_data)
#             res = ser_server.create(ser_server.validated_data)
#         return Response('ok')

# class Asset(ModelViewSet):
#     queryset = models.Asset.objects.all()
#     serializer_class = AssetSerializer

# class Asset()

class UserLogin(ViewSetMixin, APIView):
    queryset = models.UserProfile.objects.all()

    def post(self, request, *args, **kwargs):
        response = {'code': 20000, 'msg': None, 'data': None}
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        if not all([username, password]):
            response['code'] = 60010
            response['msg'] = 'Username or password error'
            return Response(response)
        user_obj_qureySet = self.queryset.filter(username=username)
        if not user_obj_qureySet:
            response['code'] = 60011
            response['msg'] = 'Username error'
            return Response(response)
        user_obj = user_obj_qureySet.first()
        if user_obj.password != password:
            response['code'] = 60012
            response['msg'] = 'Password error'
            return Response(response)
        x_token = get_token(user_obj)
        # print(x_token, type(x_token))
        response['data'] = {'token': 'admin-token'}
        return Response(response)


class UserInfo(ViewSetMixin, APIView):
    def list(self, request, *args, **kwargs):
        response = {'code': 20000, 'msg': None, 'data': None}
        response['data'] = {
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'introduction': "I am a super administrator",
            'name': "Super Admin",
            'roles': ['admin', ]
        }
        return Response(response)


class MyPage(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    # 定制传参
    page_size_query_param = 'size'
    # 最大一页的数据
    max_page_size = 40


class Server(ViewSetMixin, APIView):
    queryset = models.Server.objects.all().order_by('-asset__create_at')
    serializer_class = ServerSerializer
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        print(request.META.get('HTTP_X_TOKEN'))
        response = {'code': 20000, 'msg': None, 'data': None}
        hostname = request.query_params.get('hostname')
        # device_status_id = int(request.query_params.get('device_status_id'))
        page = MyPage()
        if hostname and hostname != 'null':
            total = 1
            instance = self.queryset.filter(hostname=hostname)
            ser_asset = self.serializer_class(instance=instance, many=True)
        else:
            total = self.queryset.count()
            page_list = page.paginate_queryset(self.queryset, request, view=self)
            # print(request.META.get('REMOTE_ADDR'))
            instance = page_list
            ser_asset = self.serializer_class(instance=instance, many=True)
        response['data'] = ser_asset.data
        response['msg'] = 'successful'
        response['total'] = total
        return Response(response)

    def create(self, request, *args, **kwargs):
        response = {'status_code': 20000, 'msg': None, 'data': None}
        ser_asset = self.serializer_class(data=request.data)
        if ser_asset.is_valid():
            print(ser_asset.validated_data)
            print('aaa')
            res = ser_asset.save()
            back_ser_asset = self.serializer_class(instance=res, many=False)
            response['data'] = back_ser_asset.data
            response['msg'] = 'successful'
            return Response(response)
        else:
            response['msg'] = ser_asset.errors
            response['status_code'] = 401
            return Response(response)

    def retrieve(self, request, *args, **kwargs):
        response = {'status_code': 20000, 'msg': None, 'data': None}
        pk = kwargs.get('pk')
        instance = self.queryset.filter(pk=pk).first()
        ser_asset = self.serializer_class(instance=instance, many=False)
        response['data'] = ser_asset.data
        response['msg'] = 'successful'
        return Response(response)

    def update(self, request, *args, **kwargs):
        response = {'status_code': 20000, 'msg': None, 'data': None}
        pk = kwargs.get('pk')
        instance = self.queryset.filter(pk=pk).first()
        ser_asset = self.serializer_class(instance=instance, data=request.data, many=False)  # 注意传输
        if ser_asset.is_valid():
            res = ser_asset.save()
            back_ser_asset = self.serializer_class(instance=res, many=False)
            response['data'] = back_ser_asset.data
            response['msg'] = 'successful'
            return Response(response)
        else:
            response['msg'] = ser_asset.errors
            response['status_code'] = 401
            return Response(response)

    def destroy(self, request, *args, **kwargs):
        response = {'status_code': 20000, 'msg': None, 'data': None}
        pk = kwargs.get('pk')
        self.queryset.filter(pk=pk).delete()
        response['msg'] = 'successful'
        return Response(response)
