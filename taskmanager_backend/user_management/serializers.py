from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.userModel
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = models.userModel.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        if password:
            instance.set_password(password)
            instance.save()
        return super().update(instance, validated_data)