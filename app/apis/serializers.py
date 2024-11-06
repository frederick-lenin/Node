from rest_framework import serializers
from django.contrib.auth.hashers import check_password, make_password
from app.models import CustomUser, Notes



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password','email')

    def create(self, data):
        try:    
            username = data['username']
            email = data['email']
            password = data['password']
            hashedpassword = make_password(password) 
            user= CustomUser.objects.create(
                username = username,
                email = email,
                password = hashedpassword
            )
            return user
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class AddNotesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Notes
        fields = ("user","title", "body")


class GetNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = "__all__"

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = "__all__"