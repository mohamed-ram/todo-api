from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'tasks', views.TaskGenericViewSet)
router.register(r'tasks', views.TaskModelViewSet)


urlpatterns = [
    # version 1
    path('tasks/', views.task_list),
    path('tasks/<int:pk>', views.task_detail),
    
    # version 2 using api_view()
    path('v2/tasks/', views.task_list_v2),
    path('v2/tasks/<int:pk>', views.task_detail_v2),
    
    # version 3 using APIView()
    path('v3/tasks/', views.TaskList.as_view()),
    path('v3/tasks/<int:pk>', views.TaskDetail.as_view()),
    
    # version 4 using mixins classes
    path('v4/tasks/', views.TaskListMixin.as_view()),
    path('v4/tasks/<int:pk>', views.TaskDetailMixin.as_view()),
    
    # version 5 using ViewSet
    path('v5/', include(router.urls)),
    
    # version 6 using GenericViewSet
    path('v6/', include(router.urls)),
    
    # version 7 using GenericViewSet
    path('v7/', include(router.urls)),
    
    
    
]
