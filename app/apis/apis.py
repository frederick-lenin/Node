from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError as JWTTokenError
from rest_framework.pagination import PageNumberPagination

from app.apis.serializers import AddNotesSerializer, GetNotesSerializer, NoteSerializer, UserRegistrationSerializer
from app.models import CustomUser, Notes




'''
    USER REGISTERATION API(USER SHOULD REGISTER WITH EMAIL , USERNAME AND PASSWORD)
'''
class UserRegistrationApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        datas = request.data
        serializer = UserRegistrationSerializer(data = datas)
        if serializer.is_valid():
            serializer.save()
            return Response ({'message': 'Registration Sucessfull'}, status = status.HTTP_200_OK)  
        return Response({'error': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)  


'''
    User can Login using respective email and password
'''

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("Invalid email or password.")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid email or password.")
        
        if not user.is_active:
            raise AuthenticationFailed("User account is not active.")
        
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
        }, status=status.HTTP_200_OK)

'''
    THIS IS BLOCK TOKEN API
'''
class LogoutApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.GET.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

'''
    THIS API WILL PROVIDE REFRESH TOKEN FOR SECURITY
'''
class RefreshTokenApiview(APIView):
    
    def get (self, request):

        refresh_token = request.GET.get('refresh')

        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token

            return Response({
                'access': str(new_access_token),
            }, status=status.HTTP_200_OK)

        except JWTTokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        

class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(
            {
                "message": "Notes retrieved successfully",
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            },
            status=status.HTTP_200_OK  
        )

class GetAddNotesApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notes = Notes.objects.filter(user=user)

        paginator = Pagination()
        paginated_notes = paginator.paginate_queryset(notes, request)

        serializer = GetNotesSerializer(paginated_notes, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = AddNotesSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data Added sucessfully", "data": serializer.data}, status= status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    
    
class RetrievePatchDeleteNotesApi(APIView):
    permission_classes = [IsAuthenticated]
    
    def get( self, request):
        try:
            id = request.GET.get('id')
            user = request.user
            note = Notes.objects.get(user = user, id = id)
            serializer = GetNotesSerializer(note)
            return Response ({'message': serializer.data}, status= status.HTTP_200_OK)
        except Exception as e:
            return Response ({'error': str(e)})
            
    def patch(self, request):
        try:
            user = request.user
            id = request.data.get('id')
            note = Notes.objects.get(id = id)
            if note.user != user:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

            serializer = NoteSerializer(note, data=request.data, partial=True)
        
            if serializer.is_valid(): 
                serializer.save() 
                return Response({'message': "Data updated successfully", 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
        except Exception as e:
            return Response ({'error': str(e)}, status= status.http)
    
    def delete(self, request):
        try:
            user = request.user 
            note_id = request.GET.get('id')

            note = Notes.objects.get(id=note_id)
            
            if note.user != user:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

            note.delete()

            return Response({'message': "Note deleted successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)