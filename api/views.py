from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin)
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TaskSerializer, TaskCustomSerializer
from tasks.models import Task
from django.views.decorators.csrf import csrf_exempt

# first method using function..
# Get all tasks and Post new task.

@csrf_exempt
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskCustomSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        serializer = TaskCustomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# Get specific task and add new one.
@csrf_exempt
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "GET":
        serializer = TaskCustomSerializer(task)
        return JsonResponse(serializer.data, safe=False, status=200)
    
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TaskCustomSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)
        
    elif request.method == "DELETE":
        task.delete()
        return HttpResponse(status=204)


# the second method.
# using api_view() & Response() from django-rest.

@api_view(['GET', 'POST'])
def task_list_v2(request):
    tasks = Task.objects.all()
    if request.method == "GET":
        serializer = TaskCustomSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = TaskCustomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail_v2(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'GET':
        serializer = TaskCustomSerializer(task)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = TaskCustomSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# The third way using APIView class.
# get task list
class TaskList(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskCustomSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskCustomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# get specific task with pk.
class TaskDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)
    
    def get(self, request, pk):
        task = self.get_object(pk=pk)
        serializer = TaskCustomSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        task = self.get_object(pk=pk)
        serializer = TaskCustomSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        task = self.get_object(pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# the forth way using mixins.
# get tasks list..
class TaskListMixin(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# get(retrieve) & update & delete specific task..
class TaskDetailMixin(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Task
    serializer_class = TaskSerializer
    # lookup_field = 'pk'
    
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    # still need some override to edit slug automatically.
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# the fifth way using ViewSets..
class TaskViewSet(ViewSet):
    
    # get task list.
    def list(self, request):
        queryset = Task.objects.all()
        serializer = TaskCustomSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # retrieve specific task.
    def retrieve(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        serializer = TaskCustomSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # create new task.
    def create(self, request):
        serializer = TaskCustomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = TaskCustomSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

# the sixth way using GenericViewSet
class TaskGenericViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskCustomSerializer
    
    # we can remove all these functions..
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request):
        return self.delete(request)


# the seventh way using ModelViewSet
class TaskModelViewSet(ModelViewSet):
    serializer_class = TaskCustomSerializer
    queryset = Task.objects.all()



