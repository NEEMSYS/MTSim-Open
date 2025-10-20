from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import UserInfo
from user.serializers import UserInfoSerializer, UserDetailSerializer
from game.models import Attend
from game.serializers import ParticipantSerializer



class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def jwt_response_payload_handler(token, user=None, request=None):
    """
    设置jwt登录之后返回token和user信息
    """
    userinfo = UserInfo.objects.get(user=user)
    attend = Attend.objects.filter(user=user)
    # 整体返回一个字典，方便根据键值对查询
    return {
        'token': token,
        # 返回一个字典，用户的用户名
        'user': UserDetailSerializer(user, context={'request': request}).data,
        # 返回一个字典，用户的详细信息
        'userinfo': UserInfoSerializer(userinfo, context={'request': request}).data,
        # 返回一个json数据, 用户的所有报名信息，返回的是此用户下的所有比赛信息，所以是一个集合，将获取到的所有字典组合成一个列表，是个数组
        'attend': ParticipantSerializer(attend,context={'request': request},many=True).data
    }


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    用户注册
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def create(self, request, *args, **kwargs):
        # 先查询是否存在已经创建的用户名
        user = User.objects.filter(username=request.data['username'])
        if user:
            return Response({'msg': '用户名已存在'}, status=status.HTTP_201_CREATED)
        # 处理发送过来的数据
        user_detail = UserDetailSerializer(data=request.data)
        if user_detail.is_valid():
            user_detail.save()
        # 此处是已经注册好的数据，获取到user,然后将user.password转为密码存储
        user = User.objects.get(username=request.data['username'])
        user.password = make_password(user.password)
        user.save()
        # 此处获取相关联的用户id,保存到数据库当中
        user_id = User.objects.filter(username=request.data['username']).first()
        row_id = user_id.id
        # 保存到用户数据库当中
        userinfo = UserInfo(user=user, user_id=row_id)
        if userinfo:
            userinfo.save()
        return Response(user_detail.errors)


class UpdatePwdApi(APIView):
    """
    修改用户密码
    """
    def patch(self, request):
        # 获取参数
        old_pwd = request.data['oldpwd']
        new_pwd = request.data['newpwd']
        user_id = request.data['userid']
        # 获得请求用户
        user = User.objects.get(id=user_id)
        # 检查原始密码是否正确
        if user.check_password(old_pwd):
            user.set_password(new_pwd)
            user.save()
        else:
            return Response(data={'msg': 'fail'}, status=status.HTTP_200_OK)
        # 返回数据
        return Response(data={'msg': 'success'}, status=status.HTTP_200_OK)

class UserinfoViewSet(viewsets.ModelViewSet):
    """
    UserinfoViewSet
    增加用户信息
    """
    # 查询集
    queryset = UserInfo.objects.all().order_by('id')
    # 序列化
    serializer_class = UserInfoSerializer

