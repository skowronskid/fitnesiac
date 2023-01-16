from django.test import SimpleTestCase
from django.urls import reverse, resolve
from events.views import home,update_exercise,search_profiles,comments_toggle,delete_comment,update_comment,add_comment,delete_exercise, list_trainings,view_training_details,add_training,update_training, all_exercises, delete_training,api_view,trainings_view

class TestUrls(SimpleTestCase):

    def test_home(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)    

    def test_list_trainings(self):
        url = reverse('list-trainings')
        self.assertEquals(resolve(url).func, list_trainings) 

    def test_add_training(self):
        url = reverse('add-training')
        self.assertEquals(resolve(url).func, add_training)  

    def test_delete_training(self):
        url = reverse("delete", args=[1])
        self.assertEquals(resolve(url).func, delete_training)

    def test_update_training(self):
        url = reverse("update", args=[1])
        self.assertEquals(resolve(url).func, update_training)
    
    def test_view_training_details(self):
        url = reverse("details", args=[1])
        self.assertEquals(resolve(url).func, view_training_details)
    
    def test_update_exercise(self):
        url = reverse("exercise-add", args=[1])
        self.assertEquals(resolve(url).func, update_exercise)

    def test_delete_exercise(self):
        url = reverse("exercise-delete", args=[1,1])
        self.assertEquals(resolve(url).func, delete_exercise)

    def test_add_comment(self):
        url = reverse("comment-add", args=[1])
        self.assertEquals(resolve(url).func, add_comment)

    def test_update_comment(self):
        url = reverse("comment-update", args=[1,1])
        self.assertEquals(resolve(url).func, update_comment)

    def test_delete_comment(self):
        url = reverse("comment-delete", args=[1,1])
        self.assertEquals(resolve(url).func, delete_comment)

    def test_comments_toggle(self):
        url = reverse("comments-toggle", args=[1])
        self.assertEquals(resolve(url).func, comments_toggle)

    def test_search_profiles(self):
        url = reverse("search-profiles")
        self.assertEquals(resolve(url).func, search_profiles)

    def test_all_exercises(self):
        url = reverse("list-exercises")
        self.assertEquals(resolve(url).func, all_exercises)

    def test_api_view(self):
        url = reverse('api_view')
        self.assertEquals(resolve(url).func, api_view)
