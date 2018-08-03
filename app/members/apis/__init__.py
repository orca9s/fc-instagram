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