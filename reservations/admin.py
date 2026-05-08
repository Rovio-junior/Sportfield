from django.contrib import admin
from .models import Sport,Terrain,Reservation,Joueur

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('terrain', 'date_reservation', 'heure_debut', 'duree', 'joueur')
    list_filter = ('date_reservation', 'terrain')
    search_fields = ('terrain__nom','joueur__nom')

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display  = ('nom_sport', 'capacite_max')
    search_fields = ('nom_sport',)

@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    list_display   = ('nom', 'type_surface', 'type_sport', 'disponibilite')
    list_filter    = ('type_sport', 'disponibilite', 'type_surface')
    search_fields  = ('nom',)
    list_editable  = ('disponibilite',) 

@admin.register(Joueur)
class JoueurAdmin(admin.ModelAdmin):
    list_display  = ('nom', 'telephone')
    search_fields = ('nom',)
    