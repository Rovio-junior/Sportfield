from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .models import Reservation, Joueur


class JoueurForm(forms.ModelForm):
    class Meta:
        model  = Joueur
        fields = ['nom','telephone']
        widgets = {
            'nom':       forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model  = Reservation
        fields = ['terrain', 'joueur', 'date_reservation', 'heure_debut', 'duree']
        widgets = {
            'terrain':         forms.Select(attrs={'class': 'form-select'}),
            'joueur':          forms.Select(attrs={'class': 'form-select'}),
            'date_reservation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_debut':     forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'duree':           forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        data    = super().clean()
        terrain = data.get('terrain')
        date    = data.get('date_reservation')
        debut   = data.get('heure_debut')
        duree   = data.get('duree')

        if not all([terrain, date, debut, duree]):
            return data

        new_start = datetime.combine(date, debut)
        new_end   = new_start + timedelta(minutes=duree)

        conflicts = Reservation.objects.filter(
            terrain=terrain,
            date_reservation=date,
        ).exclude(pk=self.instance.pk)

        for r in conflicts:
            r_start = datetime.combine(date, r.heure_debut)
            r_end   = r_start + timedelta(minutes=r.duree)
            if new_start < r_end and new_end > r_start:
                raise ValidationError(
                    f"Ce terrain est déjà réservé de {r.heure_debut} "
                    f"pour {r.duree} minutes.")
        return data