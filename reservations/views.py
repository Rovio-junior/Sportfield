# reservations/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Terrain, Sport, Reservation
from .forms import ReservationForm,JoueurForm
from django.utils import timezone

def terrain_list(request):
    terrains = Terrain.objects.select_related('type_sport').all()
    sports   = Sport.objects.all()

    q     = request.GET.get('q', '')
    sport = request.GET.get('sport', '')
    dispo = request.GET.get('dispo', '')

    if q:
        terrains = terrains.filter(nom__icontains=q)
    if sport:
        terrains = terrains.filter(type_sport__id=sport)
    if dispo in ('true', 'false'):
        terrains = terrains.filter(disponibilite=(dispo == 'true'))

    return render(request, 'reservations/terrain_list.html', {
        'terrains': terrains,
        'sports':   sports,
        'q':        q,
        'sport':    sport,
        'dispo':    dispo,
    })

def terrain_detail(request, pk):
    terrain      = get_object_or_404(Terrain, pk=pk)
    reservations = terrain.reservations.order_by(
                       'date_reservation', 'heure_debut')
    return render(request, 'reservations/terrain_detail.html', {
        'terrain':      terrain,
        'reservations': reservations,
    })

def reserver(request, terrain_id):
    terrain = get_object_or_404(Terrain, pk=terrain_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('terrain_list')
    else:
        form = ReservationForm(initial={'terrain': terrain})
    return render(request, 'reservations/reserver.html', {
        'form':    form,
        'terrain': terrain,
    })


def calendrier(request):
    today        = timezone.now().date()
    reservations = Reservation.objects.filter(date_reservation__gte=today).select_related('terrain', 'joueur').order_by('date_reservation', 'heure_debut')
    return render(request, 'reservations/calendrier.html', {'reservations': reservations,'today':today,
    })

def home(request):
    return render(request, 'reservations/home.html')


def joueur_add(request):
    if request.method == 'POST':
        form = JoueurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = JoueurForm()

    return render(request, 'joueurs/joueur_add.html', {'form': form})