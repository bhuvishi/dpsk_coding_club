from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='project-home'),
    path('account', views.account_page, name='project-account'),
    path('about', views.about_page, name='project-about'),
    path('project/<int:project_id>/', views.single_project, name='project'),
    path('project/<int:project_id>/<str:update>/', views.single_project, name='project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
]