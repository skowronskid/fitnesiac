from django.test import TestCase
from events.models import Exercise, Training, TrainingExercise, Comment

class TestModels(TestCase):

    def setUp(self):
        self.exercise1 = Exercise.objects.create(
            bodyPart='abs',
            name='shrugs'
        )

