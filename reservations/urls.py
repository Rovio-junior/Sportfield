from django.urls import path
from . import views

urlpatterns = [
    path('terrain',views.terrain_list,name='terrain_list'),
    path('',views.home,name='home'),
    path('terrain/<int:pk>/',views.terrain_detail, name='terrain_detail'),
    path('reserver/<int:terrain_id>/',views.reserver,name='reserver'),
    path('calendrier/',views.calendrier,name='calendrier'),
    path('joueurs/add/', views.joueur_add, name='joueur_add'),
]