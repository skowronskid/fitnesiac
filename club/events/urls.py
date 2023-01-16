from django.urls import path
from . import views



urlpatterns = [
    path('',views.home,name="home"),
    path('<int:year>/<str:month>',views.home,name="home"),
    
    #trainings
    path('feed', views.list_trainings, name='list-trainings'),
    path('add_training/',views.add_training, name="add-training"),
    path("<int:id>/delete/", views.delete_training, name="delete"),
    path("<int:id>/edit/", views.update_training, name="update"),
    path("<int:id>/", views.view_training_details, name="details"),
    
    #exercises
    path('<int:parent_id>/exercise/', views.update_exercise, name='exercise-add'),
    path('<int:parent_id>/exercise/<int:id>/', views.update_exercise, name='exercise-update'),
    path("<int:parent_id>/exercise/<int:id>/delete/", views.delete_exercise, name='exercise-delete'),
    path('exercises', views.all_exercises, name="list-exercises"),

    #comments
    path('<int:parent_id>/comment/', views.add_comment, name='comment-add'),
    path('<int:parent_id>/comment/<int:id>/', views.update_comment, name='comment-update'),
    path("<int:parent_id>/comment/<int:id>/delete/", views.delete_comment, name='comment-delete'),
    path('comments-toggle/<int:object_id>/', views.comments_toggle, name='comments-toggle'),
    
    #api
    path('api/', views.api_view, name='api_view'),
    
    path('search_profiles', views.search_profiles, name="search-profiles"),

]