from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from members.userserializers import UserSerializer

User=get_user_model()

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthToken(APIView):
    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')
        # authenticate실행
        user = authenticate(username=username, password=password)

        # ahthenticate가 성공한 경우
        if user:
            # Token을 가져오거나 없으면 생성
            token, _= Token.objects.get_or_create(user=user)
            # Response에 돌려줄 데이터
            data = {
                'token' : token.key,

            }
            return Response(data, status=status.HTTP_200_OK)
        # authenticate에 실패한경우
        else:
            return AuthenticationFailed()


class AuthenticationTest(APIView):
    #URL /apiusers/auth-test/
    def get(self, request):
        # request.user가 인증 된 상태일 경우, UserSerializer를 사용해 랜더링한 데이터를 보내줌
        # 인증되지 않았을 경우 NotAuthenticated Exception을 raise
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        raise NotAuthenticated('로그인 되어있지 않습니다.')

class FacebookAuthToken(APIView):
    def post(self, request):
        facebook_id = request.data.get('facebook_id')
        last_name = request.data.get('last_name')
        first_name = request.data.get('first_name')
        user, __ = User.objects.get_or_create(
            username=facebook_id,
            defaults={
                'last_name': last_name,
                'first_name': first_name,
            }
        )
        token, __ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data)
        # if User.objects.filter(username=facebook_id).exists():
        #     user = User.objects.get(username=facebook_id)
        #
        #   URL: /api/users/facebook-login/
        # request.data에 'facebook_id'와 'name'이 올 것으로 예상
        # 1. 전달받은 facebook_id에 해당하는 유저가 존재하면 해당 User에
        # 2. 존재하지 않는다면 'first_name'과 'last_name'값을 추가로 사용해 생성한 User에
        #   -> 해당하는 Token을 가져오가나 새로 생성해서 리턴
        # 결과는 Postman으로 확인


class Profile(APIView):
    def get(self, request):
        # URL: /api/users/profile/
        # request.user가 인증되어 있으면
        #   UserSerializer로 serialize한 결과를 리턴
        # 인증 안되어 있으면 NotAuthenticated예외 발생
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        raise NotAuthenticated('인증 안됨')
