from django.conf.urls import url
from django.shortcuts import redirect
from django.urls import path
from django.urls.base import get_urlconf
from .views import TagTasks,TagCreateView, Tasklist, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', Tasklist.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('tag-create/', TagCreateView.as_view(), name='tag-create'),
    path('tag-view/<str:pk>/', TagTasks.as_view() ,name='tag-view'),


]