from rest_framework.generics import GenericAPIView
from . import serializers,models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskManagement(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        try:
            
            querySet = request.data
            
            serializer = serializers.TaskSerializer(data=querySet)
            if serializer.is_valid(raise_exception=False):
                serializer.save(user = request.user)
                # Explicitly serialize the instance along with related objects
                context = {"message": "Task created successfully."}
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            context = {"message": "Error creating task"}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get("id")
        if id:
            return self.getDetail(request,id)
        elif 'status_filtered_list' in request.path:
            return self.getListWithStatusFilter(request)
        else:
            return self.getList(request)
        
    def getDetail(self, request, id,*args, **kwargs):
        try:
            
            task = models.TaskModel.objects.get(id = id)

            serializer = serializers.TaskSerializer(task)
            return Response(serializer.data,status = status.HTTP_200_OK)
        except models.TaskModel.DoesNotExist:
            context = {"message": "Task not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(str(e))
            context = {"message": "Error fetching data"}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def getList(self, request, *args, **kwargs):
        try:
            task = models.TaskModel.objects.filter(user__id=request.user.id)

            title = request.query_params.get('title')
            if title:
                task = task.filter(title__startswith=title)

            task_status = request.query_params.get('status')
            if task_status is not None:
                task = task.filter(status=task_status)

            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(task, request)
            serializer = serializers.TasklistSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except models.TaskModel.DoesNotExist:
            context = {"message": "Task not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(str(e))
            context = {"message": "Error fetching data"}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def getListWithStatusFilter(self, request, *args, **kwargs):
        try:
            task_status = request.query_params.get('status')

            if task_status is not None:
                task = models.TaskModel.objects.filter(status=task_status, user__id=request.user.id)
            else:
                task = models.TaskModel.objects.filter(user__id=request.user.id)

            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(task, request)
            serializer = serializers.TasklistSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except models.TaskModel.DoesNotExist:
            context = {"message": "Task not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(str(e))
            context = {"message": "Error fetching data"}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request, id, *args, **kwargs):
        try:
            task = models.TaskModel.objects.get(id=id)
            query_set = request.data
            serializer = serializers.TaskSerializer(task, data=query_set, partial=True)
            if serializer.is_valid(raise_exception=False):
                serializer.save()

                context = {"message": "Task updated successfully."}
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.TaskModel.DoesNotExist:
            context = {"message": "Task not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(str(e))
            context = {"message": "Error updating task"}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id, *args, **kwargs):
        try: 
            deleted_count, _ = models.TaskModel.objects.get(id=id).delete()
            if deleted_count == 0:
                return Response({'message': 'No task were deleted.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'Successfully deleted task'}, status=status.HTTP_204_NO_CONTENT)
        except models.TaskModel.DoesNotExist:
            context = {"message": "Task not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(str(e))
            context = {"message": "Error deleting task"}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)