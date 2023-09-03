from django.shortcuts import render, get_object_or_404
# __Rest__ :
from rest_framework.response import Response
from rest_framework.views import APIView # Class Base Api VIEW
from rest_framework.permissions import * 
from rest_framework.authtoken.models import Token # Class ORM Token to create database for Token 
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
# __Datetime__:
from datetime import datetime ,timedelta
# __Models__:
from .models import User
# __Serialiers__: 
from .services.serializers import UserSerializer
# __ModelViewSet_CRUD__:
from rest_framework.viewsets import ModelViewSet





# Create View:
# __Login__:
time_token = 30 # time to set expired token
expired_date = datetime.now() + timedelta(days = time_token)
expired_date.strftime("%m-%d-%Y %H:%M:%S")

@permission_classes([AllowAny])
@api_view(['POST'])
def sign_in(request):
    global expired_date # create expired_date for token
    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({
            'type':'error',
            'msg': 'Sai mật khẩu hoặc tài khoản.',
        })
    # get rest data of user object to json response
    serializer = UserSerializer(instance=user)
    # get token:
    token, created = Token.objects.get_or_create(user = user)

    # check end date for token
    if user.expired_date.strftime("%m-%d-%Y %H:%M:%S") <= datetime.now().strftime("%m-%d-%Y %H:%M:%S"):
        token.delete() # delete old token
        token = Token.objects.create(user = user) # create new token
        user.expired_date = expired_date 
        user.save()

    # user change data serializer auto change corresponding
    return Response({
        'type':'success',
        'access_token': token.key,
        'msg': serializer.data,
    })



@permission_classes([AllowAny])
@api_view(['POST'])
def sign_up(request):
    global expired_date
    # insert key 'expired_date' into request(dict)
    request.data['expired_date'] = expired_date
    # normalize name:
    serializer = UserSerializer(data=request.data)

    check_phone = User.objects.filter(phone=request.data['phone'])

    if serializer.is_valid():
        # check email and phone exist:
        if len(check_phone) == 0:
            serializer.save()
            user = User.objects.get(username = request.data['username'])
            user.set_password(request.data['password'])
            user.save() # store again pw with value is a hash.
            token = Token.objects.create(user=user)
            return Response({
                'type':'success',
                'access_token': token.key,
                'user': serializer.data
                # user change data serializer auto change corresponding
            })
        else:
            return Response({
                "type": "error",
                "message": "Email hoặc số điện thoại đã tồn tại"
            })
    return Response({
        'type': 'error'
    })



# __ALL_ROUTES__ :
from .services.routes import ROUTES
@permission_classes([AllowAny])
@api_view(['GET'])
def all_routes(request):
    return Response(ROUTES)


# __ViewSet__ : CRUD For User
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer   
    authentication_classes=[SessionAuthentication, TokenAuthentication] 
    permission_classes=[IsAuthenticated, IsAdminUser]

    



    

    

