from rest_framework import serializers
from .models import USER


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ['id', 'username', 'email', 'password', 'is_active', 'is_seller', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}, 'is_active': {'read_only': True},
                        'is_superuser': {'read_only': True}}

    def validate_passwrord(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        return value

    def validate(self, data):
        if ' ' in data['password']:
            raise serializers.ValidationError('Password must not contain spaces.')
        return data


class UserSellerSerializer(UserSerializer):

    def create(self, validated_data):
        user = USER.objects.create_user(**validated_data)
        user.is_seller = True
        user.save()
        return user


class BuyerSerializer(UserSerializer):

    def create(self, validated_data):
        validated_data.pop('is_seller')
        user = USER.objects.create_user(**validated_data)
        user.is_seller = False
        user.save()
        return user
