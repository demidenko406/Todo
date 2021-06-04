from django.forms import forms,ModelForm
import asyncio
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils.decorators import classonlymethod,sync_to_async


from .models import Task,TaskTags


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = 'all'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskForm(ModelForm):
    class Meta:
       model = Task
       fields = ['title', 'description','complete','tag']

    def __init__(self, *args, **kwargs):
       user = kwargs.pop('user')
       super(TaskForm, self).__init__(*args, **kwargs)
       self.fields['tag'].queryset = TaskTags.objects.filter(user=user)


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)

class Tasklist(LoginRequiredMixin,ListView):
    
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['tags'] = TaskTags.objects.all()
        context['tags'] = context['tags'].filter(user=self.request.user)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains = search_input)
        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    success_url = reverse_lazy('tasks')
    
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    success_url = reverse_lazy('tasks')
    
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super(TaskUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


class TagCreateView(LoginRequiredMixin,CreateView):
    model = TaskTags
    fields = ['title']
    success_url = reverse_lazy('tasks')
    template_name = 'base/tag_create.html'
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TagCreateView, self).form_valid(form)
    
class TagTasks(LoginRequiredMixin,ListView):
    model = TaskTags
    context_object_name = 'choosen_tag'
    template_name = 'base/tag-search.html'
    
    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['tags'] = TaskTags.objects.all().filter(user=self.request.user)
        context['choosen_tag'] = self.kwargs.get('pk')
        return context
