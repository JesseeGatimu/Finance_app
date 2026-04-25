from rest_framework import serializers
from django.contrib.auth import get_user_model
User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','confirm_password']
    def validate(self,data):
        if not all([data.get('username'), data.get('email') ,data.get('password'),data.get('confirm_password')]):
            raise serializers.ValidationError('All fields must be filled !')
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match !')
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email Already exists!')
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username Already exists!')
        return data
    
    def create(self,validated_data):
        validated_data.pop('confirm_password',None)
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)