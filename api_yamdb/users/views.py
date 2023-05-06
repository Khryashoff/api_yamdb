from users.models import User
from django.shortcuts import get_object_or_404
from users.serializers import SignupSerializer, TokenSerializer #UsersSerializer
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import AccessToken


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    user, _ = User.objects.get_or_create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    mail = EmailMessage(
        subject='Confirmation-code YAMDB',
        body=confirmation_code,
        from_email='from@example.com',
        to=[email]
    )
    mail.send(fail_silently=False)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    confirmation_code = serializer.data['confirmation_code']
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        token = str(AccessToken.for_user(user))
        return Response({'token': token}, status=HTTP_200_OK)
    return Response(status=400)


# from rest_framework.decorators import action
# from rest_framework.pagination import PageNumberPagination
# from rest_framework import viewsets

# from users.serializers import UsersSerializer
# from .permissions import IsAdmin


# class UsersViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UsersSerializer
#     permission_classes = [IsAdmin, ]
#     pagination_class = PageNumberPagination
#     lookup_field = 'username'

#     @action(
#         methods=['get', 'patch', ],
#         detail=False,
#         url_path='me',
#         permission_classes=[IsAuthenticated, ]
#     )
#     def user_get_his_account_data(self, request):
#         user = request.user
#         if request.method == 'GET':
#             serializer = self.get_serializer(user)
#             return Response(serializer.data)
#         data = request.data.copy()
#         data.pop('role', None)
#         serializer = self.get_serializer(
#             user,
#             data=data,
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)