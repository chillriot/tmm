import string
import random
import requests

from rest_framework import generics, status
from rest_framework.response import Response

from .models import UserMails
from .serializers import UserMailSerializer


#домен почты
MAIL_DOMAIN = 'esiix.com' 

#генеируем почтовый адрес 
def email_generator(size=8, chars=string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size))



# Регистрация и авторизация пользователя
class CreateUserMailView(generics.ListCreateAPIView):
    # Подготовка запроса к БД
    queryset = UserMails.objects.filter().only('id', 'email', )
    serializer_class = UserMailSerializer
    
    def create(self, request, *args, **kwargs):
        data = {
            'email': 'tmm.' + email_generator() + '@' + MAIL_DOMAIN
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)


        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        user_id = request.query_params.get('user_id', False)

        if not user_id:
            return Response(data={'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        queryset = queryset.filter(id=user_id)
        serializer = self.get_serializer(instance=queryset, many=True)


        return Response(data=serializer.data[0], status=status.HTTP_200_OK)

# Get Mails
class GetUserMailsView(generics.ListAPIView):
    queryset = UserMails.objects.filter().only('id', 'email', )
    serializer_class = UserMailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        user_id = request.query_params.get('user_id', False)

        if not user_id:
            return Response(data={'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        queryset = queryset.filter(id=user_id)
        serializer = self.get_serializer(instance=queryset, many=True)

        if len(serializer.data) == 0:
            return Response(data={'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        AUTH_DATA = str(serializer.data[0]['email']).split('@')
    
        req = requests.get('https://www.1secmail.com/api/v1/?action=getMessages&login='+AUTH_DATA[0]+'&domain='+AUTH_DATA[1])


        return Response(data=req.json(), status=status.HTTP_200_OK)
    
# Get Mail
class GetUserMailView(generics.ListAPIView):
    queryset = UserMails.objects.filter().only('id', 'email', )
    serializer_class = UserMailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        user_id = request.query_params.get('user_id', False)
        email_id = request.query_params.get('email_id', False)

        if not user_id:
            return Response(data={'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not email_id:
            return Response(data={'message': 'Mail not found'}, status=status.HTTP_404_NOT_FOUND)

        queryset = queryset.filter(id=user_id)
        serializer = self.get_serializer(instance=queryset, many=True)

        if len(serializer.data) == 0:
            return Response(data={'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        AUTH_DATA = str(serializer.data[0]['email']).split('@')

        # https://www.1secmail.com/api/v1/?action=readMessage&login=demo&domain=1secmail.com&id=639

        req = requests.get('https://www.1secmail.com/api/v1/?action=readMessage&login='+AUTH_DATA[0]+'&domain='+AUTH_DATA[1] + '&id=' + email_id)


        return Response(data=req.json(), status=status.HTTP_200_OK)