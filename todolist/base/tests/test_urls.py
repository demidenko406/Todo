from django.test import SimpleTestCase
from django.urls import reverse,resolve
from django.contrib.auth.views import LogoutView
from base.views import *

class TestUrls(SimpleTestCase):
    
    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class,CustomLoginView)
            
    def test_create_url(self):
        url = reverse('task-create')
        self.assertEqual(resolve(url).func.view_class,TaskCreate)
    
    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class,LogoutView)
        
    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class,RegisterPage)
    
    def test_list_url(self):
        url = reverse('tasks')
        self.assertEqual(resolve(url).func.view_class,Tasklist)
        
    def test_task_url(self):
        url = reverse('task',kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class,TaskDetail)
    
    def test_task_update_url(self):
        url = reverse('task-update',kwargs = {"pk":1})
        self.assertEqual(resolve(url).func.view_class,TaskUpdate)
        
    def test_delete_url(self):
        url = reverse('task-delete',kwargs = {"pk":1})
        self.assertEqual(resolve(url).func.view_class,DeleteView)

    def test_tag_create_url(self):
        url = reverse('tag-create')
        self.assertEqual(resolve(url).func.view_class,TagCreateView)
        
    def test_tag_view_url(self):
        url = reverse('tag-view',kwargs={'pk':"Tag1"})
        self.assertEqual(resolve(url).func.view_class,TagTasks)