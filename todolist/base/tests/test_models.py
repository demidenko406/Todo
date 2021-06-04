from django.test import TestCase
from base.models import *

class ModelsTestCase(TestCase):
    def setUp(self):
        TaskTags.objects.create(title = "Tag1")
        Task.objects.create(title = "Task1",complete = False ,description = "Des")
        

    def testTag(self):
        tag = TaskTags.objects.get(title = "Tag1")
        self.assertEqual(tag.title, "Tag1")
        
    def testTasktitle(self):
        task = Task.objects.get(title = "Task1")
        self.assertEqual(task.title, "Task1")

    def testTaskCompleted(self):
        task = Task.objects.get(title = "Task1")
        self.assertEqual(task.complete, False)
    
    def testTaskDescription(self):
        task = Task.objects.get(title = "Task1")
        self.assertEqual(task.description, "Des")
        
    