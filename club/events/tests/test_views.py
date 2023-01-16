from django.test import TestCase, Client
from django.urls import reverse
from events.models import Exercise, Training, TrainingExercise, Comment
import json

class TestViews(TestCase):
    def test_exercise_list_GET(self):
        client = Client()
        response = client.get(reverse('list-exercises'))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'events/exercise_list.html' )


