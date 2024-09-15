from django.db import models

# Create your models here.
class TaskModel(models.Model):
    user = models.ForeignKey("user_management.userModel", on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    status = models.BooleanField (default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)