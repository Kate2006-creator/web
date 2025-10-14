from django.test import TestCase
from clients.models import Client, Project 
from rest_framework.test import APIClient
from datetime import date
from model_bakery import baker

class ProjectsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_projects_list(self):
        clt = Client.objects.create(
            name="Филатова Софья Сергеевна",
            email="peach_power@mail.ru",
            sphere="Искусство"
        )
    
        project = Project.objects.create(
            name="SMM-продвижение страницы",
            client=clt,
            deadline=date(2025, 10, 31), 
            budget=50000.00,
            status="in_progress"
        )
    
        r = self.client.get('/api/projects/')
        data = r.json()
        print(data)
    
 
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], project.name)
        self.assertEqual(data[0]['client']['id'], clt.id)
        self.assertEqual(data[0]['client']['name'], clt.name)
        
