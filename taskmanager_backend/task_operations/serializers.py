from rest_framework import serializers
from . import models


class TasklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskModel
        fields = ['id','title','status']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskModel
        fields = '__all__'
